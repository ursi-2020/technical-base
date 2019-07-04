import json
import pika
import os

url_queue_host = 'localhost'
callback_dict = {}
connection = pika.BlockingConnection(pika.ConnectionParameters(host=url_queue_host))
channel = connection.channel()

def test(appfrom, appto, datetime, action, message):
    print(message)

def callback(ch, method, properties, body):
    body_json = json.load(body)
    for c in callback_dict[(body_json['from'], body_json['action'])]:
        c(body_json['from'], body_json['to'], body_json['datetime'], body_json['action'], body_json['message'])


def receive(queue_name, action, callback):

    callback_dict[(queue_name, action)].append(callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')


def send(queue_tosend, appfrom, appto, action, message):
    datetime = "05-12-19-20001201"
    channel.queue_declare(queue=queue_tosend)
    body = '{ "from":"' + appfrom +\
           '", "to":"' + appto +\
           '", "datetime":' + datetime +\
           '", "action":"' + action +\
           '", "message":"' + message + '"}'
    channel.basic_publish(exchange='', routing_key=queue_tosend, body=body)
    print(" [x] Sent message to queue name %r" % queue_tosend)
    connection.close()


if __name__ == '__main__':
    send('caisse', "caisse", "crm", "print", "toto")
    receive('caisse', 'print', test)

    channel.basic_consume(queue='caisse', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
