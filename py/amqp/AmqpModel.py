#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import datetime
import time

import amqplib.client_0_8 as amqp

class MsgHandler:
    def __init__(self):
        pass

class AmqpModel:
    def __init__(self, 
        host = "",
        userid = "", 
        password = "", 
        virtual_host = "/",
        queue = "", 
        exchange =  "",
        routing_key = "",
        ):
        self.host = host
        self.userid = userid
        self.password = password
        self.virtual_host = virtual_host
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.handler = MsgHandler() 


    def RecvData(self, callback = ""):
        conn = amqp.Connection(host = self.host, userid = self.userid, password = self.password, virtual_host = self.virtual_host)
        chan = conn.channel()
 
#        chan.access_request('/', active=True, read=True)
        chan.queue_declare(queue = self.queue, durable = True, exclusive = False, auto_delete = False)
        chan.exchange_declare(exchange = self.exchange, type = "direct", durable = True, auto_delete = False)
        chan.queue_bind(queue = self.queue, exchange = self.exchange, routing_key = self.routing_key)
        if callback == "":
            while True:
                msg = chan.basic_get(self.queue)
                if msg:
                    print msg.body
                    #self.handler.StatusParse(strBody)
                    chan.basic_ack(msg.delivery_tag)
                else:
                    time.sleep(1)
        else:
            chan.basic_consume(
                queue = self.queue,
                no_ack = True,
                callback = callback, 
                consumer_tag = callback.__name__
            )
            while True:
                chan.wait()

    def SendData(self, msg):
        msg = amqp.Message(msg)
        msg.properties["delivery_mode"] = 2
        conn = amqp.Connection(host = self.host, userid = self.userid, password = self.password, virtual_host = self.virtual_host)
        chan = conn.channel()
        chan.basic_publish(msg, exchange = self.exchange, routing_key = self.routing_key)
        chan.close() 
        conn.close()

if __name__ == "__main__":
    am = AmqpModel(
        host = "",
        userid = "", 
        password = "", 
        queue = "", 
        exchange = "", 
        routing_key = ""
    )

    def print_callback(msg):
        print type(msg)
        print "msg[%s]: %s" %(datetime.datetime.now(), msg.body)

    #am.RecvData(callback = print_callback)
    am.RecvData()

