[Sommaire](https://ursi-2020.github.io/Documentation/)

## In this tutorial you will learn how to send and handle asynchronous message.

## Let's handle asynchronous messages first

In the application A let's use a function that will catch asynchronous messages.

First import the wrappers of queue manager:

	from apipkg import queue_manager as queue

Go to the application `/asyncmsg/main.py` file.

Create a callback function that will handle asynchronous messages :

	def callback(ch, method, properties, body):
	    print(" [x] Received from queue %r" % body)

In the main function  `if __name__ == '_main_':`

Use the function : 

	queue.receive('AppB', callback)

This function will be run in the background for each asynchronous requests the queue will receive, the function callback will be applied.


Back to the function callback you added in the file `/application/asyncmsg/main.py`
if you want to add different behaviour from the callback you should say to the Application B that you need to have a particular field in the body.

Lets take an example:

From APP B  you will request that in the body of the assynchronous message you need theses fields:

	body  = '{"functionname" : "print"}'

in the `view.py` : 

	message = '{ "from":"' + os.environ['DJANGO_APP_NAME'] + '", "to":"APP A", "datetime": ' + time + ', "body": "{"functionname":"print"}"}'

Now lets handle this function in the callback of the application A

	def callback(ch, method, properties, body):
	    j = json.loads(body)
	    if j['functioname'] == 'print':
		    print(" [x] Received from queue %r" % body)


## We will see in the next section how to send a asynchronous message

In the application B you will send an asynchronous message to the application A:

Go to the file `views.py`, in the function "index(request)" create a Json message that should have all theses parameters:

**from** : from which the message is sent, you can use the variable *os.environ['DJANGO_APP_NAME']* (dont forget to import os), os.environ will get the variable stored in the fields `variables.env`

**to** : to which app the message is sent

**datetime** : date on which the request is sent, the date time will be set by get the time from the Scheduler app using the function 

	time = api.send_request('scheduler', 'clock/time')
	

**body** : a Json message that will contain particular fields that each apps need, you will need to use a standard, for this example we just put a simple String

	message = '{ "from":"' + os.environ['DJANGO_APP_NAME'] + '", "to":"AppA", "datetime": ' + time + ', "body": "Hello word"}'

Now you can send your asynchronous message by using the following function:

	queue.send('AppA',message)

Now each time you will refresh the page `/index`, an asynchronous message is sent to App A,

Previously we setuped the function call that for each asynchronous message, the callback will print the body. 
You can see the result in the terminal of the app A.

