import logging
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

import requests
from apipkg import api_manager as api
from sortedcontainers import SortedList

import clock
from log import set_logging


class Scheduler:
    time_format: str = '%d/%m/%Y-%H:%M:%S'
    recurrences: list = ["none", "minute", "hour", "day", "week"]
    actions: dict = {"none": -1, "pause": 0, "resume": 1, "reset": 2}

    schedule_logger: logging.Logger = set_logging("schedule")

    schedule_list: SortedList = SortedList()
    action_list: list = []
    zero: timedelta = timedelta()
    fake_clock: clock.Clock = None

    def __init__(self):
        self.fake_clock = clock.Clock(speed=50)

    def schedule(self, url: str, target_app: str, trigger_time: str, recurrence: str, data: str, name: str, source_app: str) -> bool:
        try:
            scheduled_datetime = datetime.strptime(trigger_time, self.time_format)
        except ValueError as e:
            self.schedule_logger.warning("Failed to schedule task due to bad datetime format for datetime: " + trigger_time + ".")
            return False

        fake_time = self.fake_clock.get_time()
        if scheduled_datetime - fake_time < self.zero:
            self.schedule_logger.warning("Failed to schedule task due to datetime (" + trigger_time + ") being prior to current datetime (" + str(fake_time) + ")")
            return False

        if recurrence is None or recurrence not in self.recurrences:
            recurrence = self.recurrences[0]

        if name is None:
            name = "default"
        if source_app is None:
            source_app = "Unknown"

        self.schedule_list.add((scheduled_datetime, url, target_app, recurrence, data, name, source_app))
        self.schedule_logger.info("Scheduling action: [TIME_REQUIRED=" + str(scheduled_datetime) + "][TIME_CURRENT=" + str(self.fake_clock.get_time()) + "][TARGET=" + str(url) + "]")

        return True

    def resume(self) -> None:
        self.action_list.append(self.actions["resume"])

    def pause(self) -> None:
        self.action_list.append(self.actions["pause"])

    def toggle(self) -> None:
        action = self.actions["resume"] if self.fake_clock.paused else self.actions["pause"]
        self.action_list.append(action)

    def start(self) -> None:
        thread = Thread(target=self.loop)
        thread.start()

    def loop(self) -> None:
        while True:
            self.next()
            self.handle_actions()

            while True:
                next_schedule = self.get()
                if next_schedule is None:
                    break
                self.send(next_schedule)
                self.reschedule(next_schedule)

    def reset(self) -> None:
        self.fake_clock.reset()

    def next(self) -> None:
        sleep(self.fake_clock.rate)
        if not self.fake_clock.paused:
            self.fake_clock.next()

    def handle_actions(self) -> None:
        for action in self.action_list:
            if action == self.actions["pause"]:
                self.fake_clock.pause()
            elif action == self.actions["resume"]:
                self.fake_clock.resume()
            elif action == self.actions["reset"]:
                self.fake_clock.reset()
                self.schedule_list.clear()
                break
        self.action_list.clear()

    def await_action(self):
        pass

    def get(self):
        if len(self.schedule_list) == 0:
            return None
        if (self.schedule_list[0][0] - self.fake_clock.get_time()) <= self.zero:
            return self.schedule_list.pop(0)
        return None

    def send(self, action: tuple) -> None:
        time = self.fake_clock.get_time()
        self.schedule_logger.info("Triggering action: [TIME_REQUIRED=" + str(action[0]) + "][TIME_CURRENT=" + str(time) + "][TARGET=" + str(action[1]) + "]")
        headers = {'Host': action[2]}
        url = api.api_services_url + action[1]
        try:
            requests.post(url, data=action[4], headers=headers)
        except Exception as e:
            self.schedule_logger.error("Failed triggering action: [TIME_REQUIRED=" + str(time) + "][TIME_CURRENT=" + str(self.fake_clock.get_time()) + "][TARGET=" + url + "]" + str(e))

    def reschedule(self, action: tuple) -> None:
        if action[3] == self.recurrences[0]:
            return
        move = timedelta(days=(action[3] == 'day'), minutes=(action[3] == 'minute'), hours=(action[3] == 'hour'), weeks=(action[3] == 'week'))
        self.schedule_list.add((action[0] + move, action[1], action[2], action[3], action[4], action[5], action[6]))
        self.schedule_logger.info("RE Scheduling action: [TIME_REQUIRED=" + str(action[0] + move) + "][TIME_CURRENT=" + str(self.fake_clock.get_time()) + "][TARGET=" + action[2] + action[1] + "]")
