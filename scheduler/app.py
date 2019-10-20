import copy
import json
import logging
import signal
from datetime import datetime

from apipkg import api_manager as api
from flask import Flask, request, abort, render_template

from log import set_logging
from scheduler import Scheduler

app = Flask(__name__)
sch: Scheduler = Scheduler()

'''
TODO
schedule month / year
'''

'''
SIGNAL
'''


def keyboard_interrupt_handler(sgn):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(sgn))
    exit(0)


'''
LOG
'''

logger: logging.Logger = set_logging("debug")

'''
ROUTES
'''

request_list = []


def add_request(req: request, name: str, description: str):
    request_list.append({
        "url": req.base_url,
        "args": req.args,
        "headers": req.headers.to_wsgi_list(),
        "body": req.get_data(as_text=True),
        "name": name,
        "description": description,
        "real_time": datetime.now().strftime(sch.time_format),
        "fake_time": sch.fake_clock.get_time().strftime(sch.time_format)
    })


@app.route('/ping', methods=['GET'])
def ping():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=json.dumps("Pong"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/activity/requests', methods=['POST'])
def get_last_requests():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=json.dumps(request_list),
        status=200,
        mimetype='application/json'
    )
    request_list.clear()
    return response


@app.route('/', methods=['GET'])
def dashboard():
    """
    Route: '/', methods=['GET', 'POST']
    :return: the dashboard of the scheduler app
    """
    add_request(request, "Dashboard", "The visual interface of the scheduler.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")

    return render_template("index.html", speed=sch.fake_clock.speed, paused=sch.fake_clock.paused, recurrence_list=sch.recurrences, time=str(sch.fake_clock.init_start.strftime(sch.time_format)))


@app.route('/schedule/size', methods=['GET'])
def get_schedule_size():
    """
    Route: '/schedule/size', methods=['GET']
    :return: returns the number of scheduled future tasks
    """
    add_request(request, "Schedule size", "The number of scheduled tasks.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=json.dumps(str(len(sch.schedule_list))),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/schedule/list', methods=['GET'])
def get_schedule_list():
    """
    Route: '/schedule/list', methods=['GET']
    :return: returns an html table with all schedules tasks, as seen in the dashboard
    """
    add_request(request, "Schedule list", "The list of scheduled tasks as html.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return render_template("schedule_table.html", scheduled_list=copy.deepcopy(sch.schedule_list))


def default(o):
    if isinstance(o, datetime):
        return datetime.strftime(o, sch.time_format)


@app.route('/schedule/json', methods=['GET'])
def get_schedule_json():
    """
    Route: '/schedule/list', methods=['GET']
    :return: returns an html table with all schedules tasks, as seen in the dashboard
    """
    add_request(request, "Schedule list", "The list of scheduled tasks as json.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    array = []
    for item in sch.schedule_list:
        array.append(item)
    response = app.response_class(
        response=json.dumps(array, default=default),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/schedule/add', methods=["POST"])
def schedule_message():
    """
    Route: '/schedule/add', methods=["POST"]
    Add a task to schedule
    Requires a json body: {"target_url"="", "target_app"="", "time"="", "recurrence"="", "data"=""}
    :return: 'Task has been scheduled' if all went well, else sends a status 422
    """
    add_request(request, "Schedule", "Schedule a task with a json body.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    parameters = request.get_json(force=True, silent=True)
    if parameters is None:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] data is empty.")
        abort(422)
    if 'target_url' not in parameters.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] target_url field not found.")
        abort(422)
    if 'time' not in parameters.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] time field not found.")
        abort(422)
    result = sch.schedule(parameters.get('target_url'), parameters.get('target_app'), parameters.get('time'), parameters.get('recurrence'), parameters.get('data'), parameters.get('name'),
                          parameters.get('source_app'))
    if not result:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Invalid fields.")
        abort(422)
    response = app.response_class(
        response=json.dumps("Task has been scheduled"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/schedule/form', methods=["POST"])
def schedule_form():
    add_request(request, "Schedule", "Schedule a task with a form.")
    form = request.form
    result = sch.schedule(form['url'], form['target'], form['time'], form['recurrence'], form['data'], form['name'], 'scheduler')
    if not result:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Invalid fields.")
        abort(422)
    response = app.response_class(
        response=json.dumps("Task has been scheduled"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/speed', methods=['GET', 'POST'])
def get_set_speed():
    """
    Route: '/clock/speed', methods=['GET', 'POST']
    If method is POST, will look for the 'new' param to set the new clock speed.
    Example: /clock/speed?new=100
    :return: the clock speed, the new clock speed if it was updated
    """
    add_request(request, "Schedule", "Schedule a task with a form.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if request.method == 'GET' or 'new' not in request.args.keys():
        return str(sch.fake_clock.speed)
    new_speed = request.args.get('new')
    new_speed = float(new_speed)
    sch.fake_clock.set_speed(new_speed)
    response = app.response_class(
        response=json.dumps(sch.fake_clock.speed),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/pause', methods=['POST'])
def pause_clock():
    """
    Route: '/clock/pause', methods=['POST']
    Pause the clock
    :return: 'success' on success or status 422 if clock was already paused.
    """
    add_request(request, "Pause clock", "Pause the clock.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    sch.pause()
    response = app.response_class(
        response=json.dumps("The pause command has been sent"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/resume', methods=['POST'])
def resume_clock():
    """
    Route: '/clock/resume', methods=['POST']
    Resume the clock
    :return: 'success' on success or status 422 if clock was already running.
    """
    add_request(request, "Resume clock", "Resume the clock.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    sch.resume()
    response = app.response_class(
        response=json.dumps("The resume command has been sent"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/switch', methods=['POST'])
def switch_state_clock():
    """
    Route: '/clock/switch', methods=['POST']
    Switch between the running and paused state of the clock.
    :return: 'success'
    """
    add_request(request, "Toggle clock", "Toggle pause / resume the clock.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    sch.toggle()
    response = app.response_class(
        response=json.dumps("The toggle command has been sent"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/time', methods=['GET'])
def get_time():
    """
    Route: '/clock/time', methods=['GET', 'POST']
    Get the current time from the clock.
    :return: a json body with the current time.
    """
    add_request(request, "Time", "Get the time.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=json.dumps(sch.fake_clock.get_time().strftime(sch.time_format)),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/info', methods=['GET'])
def get_info():
    """
    Route: '/clock/info', methods=['GET', 'POST']
    Send all the information about the clock: current time, clock speed and clock state (paused/ running)
    :return: a json body with the information
    """
    add_request(request, "Clock info", "Get infos of the clock: current time, speed, status.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=json.dumps([sch.fake_clock.get_time().strftime(sch.time_format), sch.fake_clock.speed, sch.fake_clock.paused]),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/reset', methods=['POST'])
def reset():
    add_request(request, "Reset clock", "Reset the clock.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    sch.schedule_list.clear()
    sch.reset()
    response = app.response_class(
        response=json.dumps("The reset command has been sent"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/schedule/delete', methods=['POST'])
def del_schedule():
    add_request(request, "Delete task", "Delete a scheduled task by its name.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    name = request.args.get('name', default=None, type=str)
    source = request.args.get('source', default=None, type=str)
    if source is None or name is None:
        abort(422)
    sch_list = sch.schedule_list
    i = 0
    while i < len(sch_list):
        if sch_list[i][5] == name and sch_list[i][6] == source:
            sch_list.pop(i)
            i -= 1
        i += 1
    response = app.response_class(
        response=json.dumps("The targeted tasks have been deleted"),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/app/delete', methods=['POST'])
def del_app():
    add_request(request, "Delete app's tasks", "Delete all scheduled tasks from a given app.")
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    source = request.args.get('source', default=None, type=str)
    if source is None:
        abort(422)
    sch_list = sch.schedule_list
    i = 0
    while i < len(sch_list):
        if sch_list[i][6] == source:
            sch_list.pop(i)
            i -= 1
        i += 1
    response = app.response_class(
        response=json.dumps("The targeted tasks have been deleted"),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    api.unregister('scheduler')
    api.register('http://0.0.0.0:5000', 'scheduler')
    sch.start()
    app.run(host='0.0.0.0', port=5000)
