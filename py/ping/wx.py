#!/usr/bin/python
# coding: utf-8

import os, sys, socket, struct, select, time, signal


default_timer = time.time

# ICMP parameters
ICMP_ECHOREPLY = 0 # Echo reply (per RFC792)
ICMP_ECHO = 8 # Echo request (per RFC792)
ICMP_MAX_RECV = 2048 # Max size of incoming buffer

MAX_SLEEP = 1000 # 发包间隔

def calculate_checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string): # Check for odd length
        loByte = source_string[len(source_string) - 1]
        sum += ord(loByte)

    sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


class HeaderInformation(dict):
    """ Simple storage received IP and ICMP header informations """
    def __init__(self, names, struct_format, data):
        unpacked_data = struct.unpack(struct_format, data)
        dict.__init__(self, dict(zip(names, unpacked_data)))


class Ping(object):
    def __init__(self, destination, timeout = 1000, packet_size = 55, own_id = None):
        """
        timeout 毫秒
        """
        self.destination = destination
        self.timeout = timeout
        self.packet_size = packet_size

        # 保证获取一个十六位的 own_id
        if own_id is None:
            self.own_id = os.getpid() & 0xFFFF
        else:
            self.own_id = own_id
        # 域名解析(直接是个IP地址也没有问题)
        try:
            # FIXME: Use destination only for display this line here? see: https://github.com/jedie/python-ping/issues/3
            self.dest_ip = socket.gethostbyname(self.destination)
        except socket.gaierror as e:
            self.print_unknown_host(e)
            sys.exit(-1)
        else:
            self.print_start()

        self.seq_number = 0
        self.send_count = 0
        self.receive_count = 0
        self.min_time = 999999999 # 用以记录一次ping命令中的最小时间
        self.max_time = 0.0 # 用以记录一次ping命令中的最大时间
        self.total_time = 0.0

    #--------------------------------------------------------------------------

    def print_start(self):
        """ 第一行输出，头信息 """
        print("\nPYTHON-PING %s (%s): %d data bytes" % (self.destination, self.dest_ip, self.packet_size))

    def print_unknown_host(self, e):
        """ 解析不了的错误输出 """
        print("\nPYTHON-PING: Unknown host: %s (%s)\n" % (self.destination, e.args[1]))

    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        if ip == self.destination:
            from_info = ip
        else:
            from_info = "%s (%s)" % (self.destination, ip)

        print("%d bytes from %s: icmp_seq=%d ttl=%d time=%.1f ms" % (
            packet_size, from_info, icmp_header["seq_number"], ip_header["ttl"], delay)
        )
        #print("IP header: %r" % ip_header)
        #print("ICMP header: %r" % icmp_header)

    def print_failed(self):
        """ 请求超时 """
        print("Request timed out.")

    def print_exit(self):
        """ 最后输出结果 """
        print("\n----%s PYTHON PING Statistics----" % (self.destination))

        lost_count = self.send_count - self.receive_count
        #print("%i packets lost" % lost_count)
        lost_rate = float(lost_count) / self.send_count * 100.0

        print("%d packets transmitted, %d packets received, %0.1f%% packet loss" % (
            self.send_count, self.receive_count, lost_rate
        ))

        if self.receive_count > 0:
            print("round-trip (ms)  min/avg/max = %0.3f/%0.3f/%0.3f" % (
                self.min_time, self.total_time / self.receive_count, self.max_time
            ))

        print("")

    #--------------------------------------------------------------------------
    def signal_handler(self, signum, frame):
        """
        Handle print_exit via signals
        """
        self.print_exit()
        print("\n(Terminated with signal %d)\n" % (signum))
        sys.exit(0)

    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)   # Handle Ctrl-C
        if hasattr(signal, "SIGBREAK"):
            # Handle Ctrl-Break e.g. under Windows 
            signal.signal(signal.SIGBREAK, self.signal_handler)


    #--------------------------------------------------------------------------
    def run(self, count = None, deadline = None):
        """
        send and receive pings in a loop. Stop if count or until deadline.
        """
        self.setup_signal_handler()

        while True:
            delay = self.do()

            self.seq_number += 1
            if count and self.seq_number >= count:
                break
            if deadline and self.total_time >= deadline:
                break

            # 代码不return None，该为直接return 0
            #if delay == None:
            #    delay = 0

            # Pause for the remainder of the MAX_SLEEP period (if applicable)
            if (MAX_SLEEP > delay):
                time.sleep((MAX_SLEEP - delay) / 1000.0)

        self.print_exit()

    def do(self):
        """
        Send one ICMP ECHO_REQUEST and receive the response until self.timeout
        return delay，下次运行do前 sleep的时间(ms)
        """
        try: # One could use UDP here, but it's obscure
            # 关于UDP/TCP root权限问题的选择, 感觉是使用了UDP后就不是完完全全模仿的ping命令了 
            # http://stackoverflow.com/questions/1189389/python-non-privileged-icmp
            # UDP 方式:
            # socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
            current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        except socket.error, (errno, msg):
            if errno == 1:
                # Operation not permitted - Add more information to traceback
                etype, evalue, etb = sys.exc_info()
                evalue = etype(
                    "%s - Note that ICMP messages can only be send from processes running as root." % evalue
                )
                raise etype, evalue, etb
            raise # raise the original error

        send_time = self.send_one_ping(current_socket)
        if send_time == None:
            return 0
        self.send_count += 1

        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(current_socket)
        current_socket.close()

        if receive_time:
            self.receive_count += 1
            delay = (receive_time - send_time) * 1000.0
            self.total_time += delay
            if self.min_time > delay:
                self.min_time = delay
            if self.max_time < delay:
                self.max_time = delay

            self.print_success(delay, ip, packet_size, ip_header, icmp_header)
            return delay
        else:
            self.print_failed()

    def send_one_ping(self, current_socket):
        """
        Send one ICMP ECHO_REQUEST
        """
        # http://stackoverflow.com/questions/19920535/malformed-packet-on-icmp-python
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        #  0                   1                   2                   3
        #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # |     Type      |     Code      |          Checksum             | 
        # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # |           Identifier          |        Sequence Number        |
        # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # |     Data ...
        # +-+-+-+-+-
        # 
        # http://www.cnblogs.com/gala/archive/2011/09/22/2184801.html
        # BBHHHH
        checksum = 0

        # Make a dummy header with a 0 checksum.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        #padBytes = []
        #startVal = 0x42
        #for i in range(startVal, startVal + (self.packet_size)):
        #    padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        #data = bytes(padBytes)

        # icmp Data部分
        data = chr(65)
        for i in range(66, 66 + (self.packet_size)):
            data = data + chr((i & 0xff))

        # Calculate the checksum on the data and the dummy header.
        checksum = calculate_checksum(header + data) # Checksum is in network order

        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        packet = header + data

        send_time = default_timer()

        try:
            current_socket.sendto(packet, (self.destination, 1)) # Port number is irrelevant for ICMP
        except socket.error as e:
            print("General failure (%s)" % (e.args[1]))
            current_socket.close()
            return

        return send_time

    def receive_one_ping(self, current_socket):
        """
        Receive the ping from the socket. timeout = in ms
        """
        timeout = self.timeout / 1000.0

        while True: # Loop while waiting for packet or timeout
            select_start = default_timer()
            inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
            select_duration = (default_timer() - select_start)
            if inputready == []: # timeout
                return None, 0, 0, 0, 0

            receive_time = default_timer()

            packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)
            print address

            # 20 -28 位是ICMP
            icmp_header = HeaderInformation(
                names = [
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format = "!BBHHH",
                data = packet_data[20:28]
            )

            if icmp_header["packet_id"] == self.own_id: # Our packet
                # 前20 位是IPv4
                #  0                   1                   2                   3
                #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |     Version   |     Type      |          Length               | 
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |         Identification        |Flags|   Fragment Offset       |
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |   TimeToLive  |   Protocol    |          Checksum             | 
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |                   Source IP Address                           |
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                # |                 Destination IP Address                        |
                # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                #
                ip_header = HeaderInformation(
                    names = [
                        "version", "type", "length",
                        "id", "flags", 
                        "ttl", "protocol","checksum", 
                        "src_ip",
                        "dest_ip"
                    ],
                    struct_format = "!BBHHHBBHII",
                    data = packet_data[:20]
                )
                packet_size = len(packet_data) - 28
                ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
                # XXX: Why not ip = address[0] / ip,port = address
                return receive_time, packet_size, ip, ip_header, icmp_header
            # 超时的 icmp返回, 但是正常应该都走select timeout了
            timeout = timeout - select_duration
            if timeout <= 0:
                return None, 0, 0, 0, 0

def verbose_ping(hostname, timeout=1000, count=3, packet_size=55):
    p = Ping(hostname, timeout, packet_size)
    p.run(count)


if __name__ == '__main__':
    # FIXME: Add a real CLI
    if len(sys.argv) == 1:
        print "DEMO"

        # These should work:
        verbose_ping("heise.de")
        verbose_ping("google.com")

        # Inconsistent on Windows w/ ActivePython (Python 3.2 resolves correctly
        # to the local host, but 2.7 tries to resolve to the local *gateway*)
        verbose_ping("localhost")

        # Should fail with 'getaddrinfo print_failed':
        verbose_ping("foobar_url.foobar")

        # Should fail (timeout), but it depends on the local network:
        verbose_ping("192.168.255.254")

        # Should fails with 'The requested address is not valid in its context':
        verbose_ping("0.0.0.0")
    elif len(sys.argv) == 2:
        verbose_ping(sys.argv[1])
    else:
        print "Error: call ./ping.py domain.tld"
