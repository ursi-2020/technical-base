[home](../index.md)

# Scheduler

## Routes

### Dashboard
```
Route: '/', methods=['GET']
:return: the dashboard of the scheduler app
```

### Info
```
Route: '/clock/info', methods=['GET']
Send all the information about the clock: current time, clock speed and clock state (paused/ running)
:return: a json body with the information
```

### List of schedules
```
Route: '/schedule/list', methods=['GET']
:return: returns an html table with all schedules tasks, as seen in the dashboard
```

### Size of schedule list
```
Route: '/schedule/size', methods=['GET']
:return: returns the number of scheduled future tasks
```

### Clock speed
```
Route: '/clock/speed', methods=['GET', 'POST']
If method is POST, will look for the 'new' param to set the new clock speed.
Example: /clock/speed?new=100
:return: the clock speed, the new clock speed if it was updated
```

### Clock time
```
Route: '/clock/time', methods=['GET']
Get the current time from the clock with format '%d/%m/%Y-%H:%M:%S'.
:return: a json body with the current time.
```

### Pause clock
```
Route: '/clock/pause', methods=['POST']
Pause the clock
:return: 'success' on success or status 422 if clock was already paused.
```

### Resume clock
```
Route: '/clock/resume', methods=['POST']
Resume the clock
:return: 'success' on success or status 422 if clock was already running.
```

### Schedule
```
Route: '/schedule/add', methods=["POST"]
Add a task to schedule
Requires a json body: {"target_url"="", "target_app"="", "time"="", "recurrence"="", "data"=""}
:return: 'Task has been scheduled' if all went well, else sends a status 422
```

### Pause / resume clock
```
Route: '/clock/switch', methods=['POST']
Switch between the running and paused state of the clock.
:return: 'success'
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
def schedule_task(host, url, time, recurrence, data):
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    headers = {'Host': 'scheduler'}
    data = {"target_url": url, "target_app": host, "time": time_str, "recurrence": recurrence, "data": data}
    r = requests.post(api.api_services_url + 'schedule/add', headers = headers, json = data)
    print(r.status_code)
    print(r.text)
    return r.text
```
