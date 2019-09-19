from datetime import datetime, timedelta
from sortedcontainers import SortedList
from time import sleep
from threading import Thread
from log import set_logging
import clock
import requests
import logging
from apipkg import api_manager as api


class Scheduler:
    time_format: str = '%d/%m/%Y-%H:%M:%S'
    schedule_list: SortedList = SortedList()
    zero: timedelta = timedelta()
    fake_clock: clock.Clock = None
    recurrences: list = ["none", "minute", "hour", "day", "week"]
    schedule_logger: logging.Logger = set_logging("schedule")

    def __init__(self, fake_clock: clock.Clock):
        self.fake_clock = fake_clock
        thread = Thread(target=self.trigger)
        thread.start()

    def close(self):
        # print(e) # TODO Logger
        pass

    def schedule(self, url: str, target_app: str, trigger_time: str, recurrence: str, data: str, name: str, source_app: str) -> bool:
        try:
            scheduled_datetime = datetime.strptime(trigger_time, self.time_format)
        except ValueError as e:
            print(e)  # TODO Logger
            return False

        if scheduled_datetime - self.fake_clock.get_time() < self.zero:
            return False

        if recurrence is None or not recurrence in self.recurrences:
            recurrence = self.recurrences[0]

        if name is None:
            name = "default"
        if source_app is None:
            source_app = "Unknown"

        self.schedule_list.add((scheduled_datetime, url, target_app, recurrence, data, name, source_app))

        self.schedule_logger.info(
            "Scheduling action: [TIME_REQUIRED=" + str(scheduled_datetime) + "][TIME_CURRENT=" + str(self.fake_clock.get_time()) + "][TARGET=" + str(
                url) + "]")
        return True

    def trigger(self) -> None:
        while True:
            if len(self.schedule_list) != 0:
                time = self.fake_clock.get_time()
                while len(self.schedule_list) != 0 and (self.schedule_list[0][0] - time) <= self.zero:
                    action = self.schedule_list.pop(0)
                    self.send(action, time)
            sleep(0.1)

    def send(self, action: tuple, time: datetime) -> None:
        self.schedule_logger.info("Triggering action: [TIME_REQUIRED=" + str(action[0]) + "][TIME_CURRENT=" + str(time) + "][TARGET=" + str(action[1]) + "]")
        self.reschedule(action)
        headers = {'Host': action[2]}
        thread = Thread(target=self.post, args=(api.api_services_url + action[1], action[4], headers, action[0], time))
        thread.start()

    def post(self, url, data, headers, req, time):
        try:
            requests.post(url, data=data, headers=headers)
        except Exception:
            print("fail")

    def reschedule(self, action: tuple) -> None:
        print(action)
        if action[3] == self.recurrences[0]:
            return
        move = timedelta(days=(action[3] == 'day'), minutes=(action[3] == 'minute'), hours=(action[3] == 'hour'), weeks=(action[3] == 'week'))
        print(move)
        self.schedule_list.add((action[0] + move, action[1], action[2], action[3], action[4], action[5], action[6]))
