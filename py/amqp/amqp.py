#!/usr/bin/python
#-*- Encoding: utf-8 -*-
import datetime

import amqplib.client_0_8 as amqp
""" amqp_consumer """ 
conn = amqp.Connection(
    host = "localhost:5672 ", 
    userid = "guest",
    password = "guest", 
    virtual_host = "/", 
    insist = False 
) 
# insist on connecting to server
# In a configuration with multiple load-sharing servers,
# the server may respond to a Connection.Open method
# with a Connection.Redirect. The insist option tells
# the server that the client is insisting on a
# connection to the specified server.
# 
# When the client uses the insist option, the server
# SHOULD accept the client connection unless it is
# technically unable to do so.

# .channel(x)来指定channel标识，其中x是你想要使用的channel标识。通常情况下，
# 推荐使用.channel()方法来自动分配 channel标识，以便防止冲突。

chan = conn.channel()
chan.queue_declare(
    queue = "po_box", 
    durable = True, # durable的（重启之后会重新建立）
    exclusive = False, # 如果设置成True，只有创建这个队列的消费者程序才允许连接到该队列。这种队列对于这个消费者程序是私有的
    auto_delete = False # 并且最后一个消费者断开的时候不会自动删除
)
chan.exchange_declare(
    exchange = "sorting_room", 
    type = "direct", # 交换机的类型 fanout, direct 和 topic.
    durable = True,
    auto_delete = False
)
chan.queue_bind(
    queue = "po_box", 
    exchange = "sorting_room",
    routing_key = "jason"
)

# 1)取消息
msg = chan.basic_get("po_box") 
# 如果队列当中没有消息，chan.basic_get()会返回None
if msg:
    print msg.body 
    chan.basic_ack(msg.delivery_tag)

# 2)取消息 回调
# chan.basic_consume()注册一个新消息到达的回调。
def recv_callback(msg):
    print 'Received: ' + msg.body 

chan.basic_consume(
    queue = 'po_box', 
    no_ack = True, # 这个参数可以传给chan.basic_get()和chan.basic_consume()， 默认是false。
    callback = recv_callback, 
    consumer_tag = "testtag"
) 
while True:
    # chan.wait() 放在一个无限循环里面，这个函数会等待在队列上，直到下一个消息到达队列。
    chan.wait() 

# chan.basic_cancel() 用来注销该回调函数
# 参数consumer_tag 当中指定的字符串和chan.basic_consume() 注册的一致
chan.basic_cancel("testtag")

# no_ack 这个参数可以传给chan.basic_get()和chan.basic_consume()， 默认是false。
# 当从队列当中取出一个消息的时候，RabbitMQ需要应用显式地回馈说已经获取到了该消息。
# 如果一段时间内不回馈，RabbitMQ 会将该消息重新分配给另外一个绑定在该队列上的消费者。
# 另一种情况是消费者断开连接，但是获取到的消息没有回馈，则RabbitMQ同样重新分配。
# 如果将no_ack 参数设置为true，则py-amqplib会为下一个AMQP请求添加一个no_ack属性，告诉AMQP服务器不需要等待回馈
# 但是，大多数时候，你也许想要自己手工发送回馈，
# 例如，需要在回馈之前将消息存入数据库。回馈通常是通过调用chan.basic_ack()方法，使用消息的 delivery_tag 属性作为参数。

""" amqp_publisher"""

msg = amqp.Message("Test Message[%s]" % datetime.datetime.now())
# delivery_mode属性为2，因为队列和交换机都设置为durable的，这个设置将保证消息能够持久化，
# 也就是说，当它还没有送达消费者之前如果RabbitMQ重启则它能够被恢复。
msg.properties["delivery_mode"] = 2
chan.basic_publish(msg, exchange = "sorting_room", routing_key = "jason")

chan.close()
conn.close()




