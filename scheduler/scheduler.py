from datetime import datetime, timedelta
from sortedcontainers import SortedList
from time import sleep
from threading import Thread
from log import set_logging
import clock
import requests
import logging


class Scheduler:
    time_format: str = '%d/%m/%Y-%H:%M:%S'
    schedule_list: SortedList = SortedList()
    zero: timedelta = timedelta()
    fake_clock: clock.Clock = None
    recurrences: list = ["none", "minute", "hour", "day", "week", "month", "year"]
    schedule_logger: logging.Logger = set_logging("schedule")

    def __init__(self, fake_clock: clock.Clock):
        self.fake_clock = fake_clock
        thread = Thread(target=self.trigger)
        thread.start()

    def close(self):
        # print(e) # TODO Logger
        pass

    def schedule(self, url: str, trigger_time: str, recurrence: str, data: str) -> bool:
        try:
            scheduled_datetime = datetime.strptime(trigger_time, self.time_format)
        except ValueError as e:
            print(e)  # TODO Logger
            return False

        if scheduled_datetime - self.fake_clock.get_time() < self.zero:
            return False

        if recurrence is None or not recurrence in self.recurrences:
            recurrence = self.recurrences[0]

        self.schedule_list.add((scheduled_datetime, url, recurrence, data))

        self.schedule_logger.info(
            "Scheduling action: [TIME_REQUIRED=" + str(scheduled_datetime) + "][TIME_CURRENT=" + str(self.fake_clock.get_time()) + "][TARGET=" + str(
                url) + "]")
        return True

    def trigger(self) -> None:
        while True:
            if len(self.schedule_list) != 0:
                time = self.fake_clock.get_time()
                while len(self.schedule_list) != 0 and self.schedule_list[0][0] - time <= self.zero:
                    action = self.schedule_list.pop(0)
                    thread = Thread(target=self.send, args=(action, time))
                    thread.start()
            sleep(0.1)

    def send(self, action: tuple, time: datetime) -> None:
        self.schedule_logger.info(
            "Triggering action: [TIME_REQUIRED=" + str(action[0]) + "][TIME_CURRENT=" + str(time) + "][TARGET=" + str(
                action[1]) + "]")
        self.reschedule(action)
        try:
            requests.post(action[1], data=action[2])
        except Exception as e:
            self.schedule_logger.info(
                "Triggering action: [TIME_REQUIRED=" + str(action[0]) + "][TIME_CURRENT=" + str(
                    time) + "][TARGET=" + str(
                    action[1]) + "]" + "Failed ===>" + e)

    def reschedule(self, action: tuple) -> None:
        print(action)
        if action[2] == 'none':
            return
        move: timedelta = None
        move = timedelta(days=(action[2] == 'day'), minutes=(action[2] == 'minute'), hours=(action[2] == 'hour'),
                         weeks=(action[2] == 'week'))
        print(move)
        self.schedule_list.add((action[0] + move, action[1], action[2], action[3]))
