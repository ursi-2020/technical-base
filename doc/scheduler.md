[home](../index.md)

# Scheduler

## Usage

The scheduler is used to get all data related to time and to schedule tasks.
It is registered to the api manager with the name ```scheduler```.


You can access a visual version of the scheduler through the port ```5000``` and the route ```/```.


It provides a number of routes that are described below. The routes whose titles are preceded by ```*``` should only be used for development purposes.

A function to help you schedule your tasks is given at the end of this dowument.

## Routes

### Info
```
Route: '/clock/info', methods=['GET']
Send all the information about the clock: current time, clock speed and clock state (paused/ running)
:return: a json body with the information
```

### Clock time
```
Route: '/clock/time', methods=['GET']
Get the current time from the clock with format '%d/%m/%Y-%H:%M:%S'.
:return: a json body with the current time.
```

### Schedule
```
Route: '/schedule/add', methods=["POST"]
Add a task to schedule
Requires a json body: {"target_url"="", "target_app"="", "time"="", "recurrence"="", "data"=""}
:return: 'Task has been scheduled' if all went well, else sends a status 422
```

### *List of schedules
```
Route: '/schedule/list', methods=['GET']
:return: returns an html table with all schedules tasks, as seen in the dashboard
```

### *Size of schedule list
```
Route: '/schedule/size', methods=['GET']
:return: returns the number of scheduled future tasks
```

### *Clock speed
```
Route: '/clock/speed', methods=['GET', 'POST']
If method is POST, will look for the 'new' param to set the new clock speed.
Example: /clock/speed?new=100
:return: the clock speed, the new clock speed if it was updated
```

### *Dashboard
```
Route: '/', methods=['GET']
:return: the dashboard of the scheduler app
```

### *Pause clock
```
Route: '/clock/pause', methods=['POST']
Pause the clock
:return: 'success' on success or status 422 if clock was already paused.
```

### *Resume clock
```
Route: '/clock/resume', methods=['POST']
Resume the clock
:return: 'success' on success or status 422 if clock was already running.
```

### *Pause / resume clock
```
Route: '/clock/switch', methods=['POST']
Switch between the running and paused state of the clock.
:return: 'success'
```

### *Reset
```
Route: '/reset', methods=['POST']
Reset the scheduler. Set the clock back to its intial time, at its intial speed.
Removes all scheduled tasks.
:return: 'OK'
```

### *Delete task
```
Route: '/schedule/delete', methods=['POST']
?name=<name>&source=<source>
name: str => the name of the task to delete.
source: str => the source application this task belongs to.
Delete a scheduled task by its name and source.
:return: 'OK'
```

### *Delete all app's tasks
```
Route: '/app/delete', methods=['POST']
?source=<source>
source: str => the source application.
Delete all scheduled tasks belonging to the 'source' application.
:return: 'OK'
```


## Functions

### How to schedule a task ?
The function below helps you scheduling the task.
The paramaters to input are the following:
```
host: string => The app targetted by the scheduled task.
```
```
url: string => URL in the targetted app.
```
```
time: datetime objet => The time at which the task should be executed.
```
```
recurrence: string => The recurrence of the task: ["none", "minute", "hour", "day", "week", "month", "year"].
None means it will be executed only once, minute means it will be executed every minute, ...
```
```
data: string => Optional data that can be passed to the targetted app through the request's body.
```
```
source: string => The source of the schedule, your app name.
It should be exactly the same for all schedules your app makes.
```
```
name: string => Used to identify the schedules individually.
Each schedules of your app must have a unique name. You should name them correctly for clarity.
```
```
def schedule_task(host, url, time, recurrence, data, source, name):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data, "source_app": source, "name": name}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text
```
