import pika

url_queue_host = 'localhost'


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


def receive(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=url_queue_host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def send(queue_tosend, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=url_queue_host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_tosend)

    channel.basic_publish(exchange='', routing_key=queue_tosend, body=message)
    print(" [x] Sent message to queue name %r" % queue_tosend)
    connection.close()


#if __name__ == '__main__':
 #  message = '{ "from":"caisse", "to":"caisse", "datetime": "05-12-19-20001201", "body": "Hello word"}'
 # message2 = '{ "from":"caisse", "to":"crm", "datetime": "05-12-19-20001201", "body": "Hello word 2"}'
 #  send('caisse', message)
 #  send('crm', message2)
 #  receive('caisse')
 # receive('crm')
#