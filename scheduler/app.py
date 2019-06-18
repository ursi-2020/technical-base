from flask import Flask, request, abort, render_template, jsonify
from scheduler import Scheduler
from clock import Clock
import signal
import logging
from log import set_logging
#import api_manager as api

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
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return render_template("index.html", speed=clk.speed, paused=clk.paused)


@app.route('/schedule/size', methods=['GET'])
def get_schedule_size():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return str(len(sch.schedule_list))


@app.route('/schedule/list', methods=['GET'])
def get_schedule_list():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return render_template("schedule_table.html", scheduled_list=sch.schedule_list)


@app.route('/schedule/add', methods=["POST"])
def schedule_message():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if 'target_url' not in request.args.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] targe_url field not found.")
        abort(422)
    if 'time' not in request.args.keys():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] time field not found.")
        abort(422)
    result = sch.schedule(request.args.get('target_url'), request.args.get('time'), request.args.get('recurrence'), request.get_data(as_text=True))
    if not result:
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Invalid fields.")
        abort(422)
    return "Task has been scheduled"


@app.route('/clock/speed', methods=['GET', 'POST'])
def get_set_speed():
    print(request)
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if request.method == 'GET' or not 'new' in request.args.keys():
        return str(clk.speed)
    new_speed = request.args.get('new')
    new_speed = float(new_speed)
    clk.set_speed(new_speed)
    return str(clk.speed)


@app.route('/clock/pause', methods=['POST'])
def pause_clock():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.pause():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Clock is not running.")
        abort(422)
    return 'success'


@app.route('/clock/resume', methods=['POST'])
def resume_clock():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.resume():
        logger.warning("Invalid HTTP request [Method = " + request.method + ", URL = " + request.url + "] Clock is not paused.")
        abort(422)
    return 'success'


@app.route('/clock/switch', methods=['POST'])
def switch_state_clock():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    if not clk.resume():
        clk.pause()
    return 'success'


@app.route('/clock/time', methods=['GET', 'POST'])
def get_time():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    response = app.response_class(
        response=str('"' + clk.get_time().strftime(sch.time_format) + '"'),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/clock/info', methods=['GET'])
def get_info():
    logger.info("HTTP request [Method = " + request.method + ", URL = " + request.url + "]")
    return jsonify((str(clk.get_time().strftime(sch.time_format)), str(clk.speed), str(clk.paused)))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    #api.unregister('scheduler')
    #api.register('http://localhost:5000', 'scheduler')
    app.run(host='localhost', port=5000)
