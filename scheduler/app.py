import sys
sys.path.insert(0,'../apimanager')
from flask import Flask, request, abort, render_template, jsonify
from scheduler import Scheduler
from clock import Clock
import signal
import logging
from log import set_logging
import api_manager as api
import json

app = Flask(__name__)
speed = 50.0
clk: Clock = Clock(speed=speed)
sch: Scheduler = Scheduler(clk)

'''
SIGNAL
'''


def keyboard_interrupt_handler(sgn, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(sgn))
    sch.close()
    exit(0)


'''
LOG
'''

logger: logging.Logger = set_logging("debug")

'''
ROUTES
'''


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """
    Route: '/', methods=['GET', 'POST']
    :return: the dashboard of the scheduler app
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return render_template("index.html", speed=clk.speed, paused=clk.paused)


@app.route('/schedule/size', methods=['GET'])
def get_schedule_size():
    """
    Route: '/schedule/size', methods=['GET']
    :return: returns the number of scheduled future tasks
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return str(len(sch.schedule_list))


@app.route('/schedule/list', methods=['GET'])
def get_schedule_list():
    """
    Route: '/schedule/list', methods=['GET']
    :return: returns an html table with all schedules tasks, as seen in the dashboard
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return render_template("schedule_table.html", scheduled_list=sch.schedule_list)


@app.route('/schedule/add', methods=["POST"])
def schedule_message():
    """
    Route: '/schedule/add', methods=["POST"]
    Add a task to schedule
    Requires a json body: {"target_url"="", "target_app"="", "time"="", "recurrence"="", "data"=""}
    :return: 'Task has been scheduled' if all went well, else sends a status 422
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    parameters = request.get_json(force=True, silent=True)
    if parameters is None:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] data is empty.")
        abort(422)
    if 'target_url' not in parameters.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] targe_url field not found.")
        abort(422)
    if 'time' not in parameters.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] time field not found.")
        abort(422)
    result = sch.schedule(parameters.get('target_url'), parameters.get('time'), parameters.get('recurrence'), parameters.get('data'))
    if not result:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Invalid fields.")
        abort(422)
    return "Task has been scheduled"


@app.route('/clock/speed', methods=['GET', 'POST'])
def get_set_speed():
    """
    Route: '/clock/speed', methods=['GET', 'POST']
    If method is POST, will look for the 'new' param to set the new clock speed.
    Example: /clock/speed?new=100
    :return: the clock speed, the new clock speed if it was updated
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if request.method == 'GET' or not 'new' in request.args.keys():
        return str(clk.speed)
    new_speed = request.args.get('new')
    new_speed = float(new_speed)
    clk.set_speed(new_speed)
    return str(clk.speed)


@app.route('/clock/pause', methods=['POST'])
def pause_clock():
    """
    Route: '/clock/pause', methods=['POST']
    Pause the clock
    :return: 'success' on success or status 422 if clock was already paused.
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.pause():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Clock is not running.")
        abort(422)
    return 'success'


@app.route('/clock/resume', methods=['POST'])
def resume_clock():
    """
    Route: '/clock/resume', methods=['POST']
    Resume the clock
    :return: 'success' on success or status 422 if clock was already running.
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.resume():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Clock is not paused.")
        abort(422)
    return 'success'


@app.route('/clock/switch', methods=['POST'])
def switch_state_clock():
    """
    Route: '/clock/switch', methods=['POST']
    Switch between the running and paused state of the clock.
    :return: 'success'
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.resume():
        clk.pause()
    return 'success'


@app.route('/clock/time', methods=['GET', 'POST'])
def get_time():
    """
    Route: '/clock/time', methods=['GET', 'POST']
    Get the current time from the clock.
    :return: a json body with the current time.
    """
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=str('"' + clk.get_time().strftime(sch.time_format) + '"'),
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
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return jsonify((str(clk.get_time().strftime(sch.time_format)), str(clk.speed), str(clk.paused)))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    api.unregister('scheduler')
    api.register('http://localhost:5000', 'scheduler')
    app.run(host='localhost', port=5000)
