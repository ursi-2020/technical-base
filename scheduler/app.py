from flask import Flask, request, abort
import scheduler
import signal
import clock

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    return "Hello World!"


@app.route('/schedule', methods=["POST"])
def schedule_message():
    if not 'target_url' in request.args.keys():
        abort(422)
    if not 'time' in request.args.keys():
        abort(422)

    result = scheduler.schedule(request.args.get('target_url'), request.args.get('time'),
                                request.get_data(as_text=True))

    if not result:
        abort(422)

    return "Task has been scheduled"


@app.route('/time')
def get_time():
    return str(clock.clock.get_time().strftime(scheduler.time_format))


def keyboard_interrupt_handler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    scheduler.close()
    exit(0)


if __name__ == '__main__':
    scheduler.init()
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    clock.clock = clock.Clock(speed=10)
    app.run(host='localhost', port=5000)
