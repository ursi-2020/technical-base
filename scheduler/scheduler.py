from urllib.parse import urlparse
from datetime import datetime, timedelta
from sortedcontainers import SortedList
from time import sleep
from threading import Thread
import clock
import requests

time_format: str = '%d/%m/%Y-%H:%M:%S'
schedule_list: SortedList = SortedList()
zero: timedelta = timedelta()


def init():
    thread = Thread(target=trigger)
    thread.start()
    pass


def close():
    pass


def schedule(url: str, trigger_time: str, data: str) -> bool:
    target_url = urlparse(url)
    scheduled_datetime: datetime = None
    try:
        scheduled_datetime = datetime.strptime(trigger_time, time_format)
    except ValueError as e:
        print(e)  # TODO Logger
        return False

    if scheduled_datetime - clock.clock.get_time() < zero:
        return False

    schedule_list.add((scheduled_datetime, target_url, data))
    return True


def trigger():
    while True:
        if len(schedule_list) != 0:
            time = clock.clock.get_time()
            while len(schedule_list) != 0 and schedule_list[0][0] - time <= zero:
                action = schedule_list.pop(0)
                print("Triggering action: [TIME_REQUIRED=" + str(action[0]) + "][TIME_CURRENT=" + str(
                    time) + "][TARGET=" + str(action[1]) + "]")  # TODO Logger
                try:
                    requests.post(action[1], data=action[2])
                except Exception:
                    # print(e) # TODO Logger
                    pass
        sleep(1)
