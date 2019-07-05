[home](../index.md)

# Scheduler

## Functions:

### dashboard()
```
Route: '/', methods=['GET', 'POST']
:return: the dashboard of the scheduler app
```

### get_info()
```
Route: '/clock/info', methods=['GET', 'POST']
Send all the information about the clock: current time, clock speed and clock state (paused/ running)
:return: a json body with the information
```

### get_schedule_list()
```
Route: '/schedule/list', methods=['GET']
:return: returns an html table with all schedules tasks, as seen in the dashboard
```

### get_schedule_size()
```
Route: '/schedule/size', methods=['GET']
:return: returns the number of scheduled future tasks
```

### get_set_speed()
```
Route: '/clock/speed', methods=['GET', 'POST']
If method is POST, will look for the 'new' param to set the new clock speed.
Example: /clock/speed?new=100
:return: the clock speed, the new clock speed if it was updated
```

### get_time()
```
Route: '/clock/time', methods=['GET', 'POST']
Get the current time from the clock.
:return: a json body with the current time.
```

### pause_clock()
```
Route: '/clock/pause', methods=['POST']
Pause the clock
:return: 'success' on success or status 422 if clock was already paused.
```

### resume_clock()
```
Route: '/clock/resume', methods=['POST']
Resume the clock
:return: 'success' on success or status 422 if clock was already running.
```

### schedule_message()
```
Route: '/schedule/add', methods=["POST"]
Add a task to schedule
Requires a json body: {"target_url"="", "target_app"="", "time"="", "recurrence"="", "data"=""}
:return: 'Task has been scheduled' if all went well, else sends a status 422
```

### switch_state_clock()
```
Route: '/clock/switch', methods=['POST']
Switch between the running and paused state of the clock.
:return: 'success'
```
