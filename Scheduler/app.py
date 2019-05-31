from flask import Flask, request, abort, render_template, jsonify
from scheduler import Scheduler
from clock import Clock
import signal
import sys

app = Flask(__name__)
speed = 50.0
if len(sys.argv) > 1:
    speed = sys.argv[1]
clk: Clock = Clock(speed=speed)
sch: Scheduler = Scheduler(clk)

'''
ROUTES
'''


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # print(e) # TODO Logger
    return render_template("index.html", speed=clk.speed, paused=clk.paused)


@app.route('/schedule/size', methods=['GET'])
def get_schedule_size():
    return str(len(sch.schedule_list))


@app.route('/schedule/list', methods=['GET'])
def get_schedule_list():
    return render_template("schedule_table.html", scheduled_list=sch.schedule_list)


@app.route('/schedule/add', methods=["POST"])
def schedule_message():
    # print(e) # TODO Logger
    if 'target_url' not in request.args.keys():
        abort(422)
    if 'time' not in request.args.keys():
        abort(422)
    result = sch.schedule(request.args.get('target_url'), request.args.get('time'), request.args.get('recurrence'),
                          request.get_data(as_text=True))
    if not result:
        abort(422)
    return "Task has been scheduled"


@app.route('/clock/speed', methods=['GET', 'POST'])
def get_set_speed():
    print(request)
    # print(e) # TODO Logger
    if request.method == 'GET' or not 'new' in request.args.keys():
        return str(clk.speed)
    new_speed = request.args.get('new')
    new_speed = float(new_speed)
    clk.set_speed(new_speed)
    return str(clk.speed)


@app.route('/clock/pause', methods=['POST'])
def pause_clock():
    if not clk.pause():
        abort(422)
    return 'success'


@app.route('/clock/resume', methods=['POST'])
def resume_clock():
    if not clk.resume():
        abort(422)
    return 'success'


@app.route('/clock/switch', methods=['POST'])
def switch_state_clock():
    if not clk.resume():
        clk.pause()
    return 'success'

@app.route('/clock/time', methods=['GET', 'POST'])
def get_time():
    # print(e) # TODO Logger
    return str(clk.get_time().strftime(sch.time_format))


@app.route('/clock/info', methods=['GET'])
def get_info():
    return jsonify((str(clk.get_time().strftime(sch.time_format)), str(clk.speed), str(clk.paused)))


def keyboard_interrupt_handler(sgn, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(sgn))
    sch.close()
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    app.run(host='localhost', port=5000)
