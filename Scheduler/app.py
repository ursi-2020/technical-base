from flask import Flask, request, abort, render_template
from scheduler import Scheduler
from clock import Clock
import signal

app = Flask(__name__)
clk : Clock = None
sch : Scheduler = None


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # print(e) # TODO Logger
    return render_template("index.html", scheduled_list = sch.schedule_list, time = clk.get_time(), speed = clk.speed, paused = clk.paused)

@app.route('/speed', methods=['GET', 'POST'])
def speed():
    print(request)
    # print(e) # TODO Logger
    if not 'new' in request.args.keys():
        return str(clk.speed)
    new_speed = request.args.get('new')
    new_speed = float(new_speed)
    clk.set_speed(new_speed)
    return str(clk.speed)

@app.route('/schedule', methods=["POST"])
def schedule_message():
    # print(e) # TODO Logger
    if not 'target_url' in request.args.keys():
        abort(422)
    if not 'time' in request.args.keys():
        abort(422)

    result = sch.schedule(request.args.get('target_url'), request.args.get('time'),
                                request.args.get('recurrence'), request.get_data(as_text=True))

    if not result:
        abort(422)

    return "Task has been scheduled"


@app.route('/time')
def get_time():
    # print(e) # TODO Logger
    return str(clk.get_time().strftime(sch.time_format))


def keyboard_interrupt_handler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    sch.close()
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    clk = Clock(speed=10)
    sch = Scheduler(clk)
    app.run(host='localhost', port=5000)
