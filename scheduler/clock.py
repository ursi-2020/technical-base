from datetime import datetime
import copy

class Clock:

    start_time: datetime = None
    speed_init: float = 1

    paused: bool = False
    paused_time: datetime = None
    real_start: datetime = None
    start: datetime = None
    speed: float = 1

    def __init__(self, start_time: datetime = datetime(2019, 1, 7, 1), speed: float = 1) -> None:
        self.start_time = start_time
        self.speed_init = speed

        self.real_start = datetime.now()
        self.start = copy.deepcopy(start_time)
        self.speed = speed if speed > 0 else 1

    def reset(self):
        self.real_start = datetime.now()
        self.start = copy.deepcopy(self.start_time)
        self.speed = self.speed_init if self.speed_init > 0 else 1
        self.paused = False

    def set_speed(self, speed: float) -> float:
        real_current = datetime.now()
        current = self.get_time(real_current)
        self.speed = speed if speed > 0 else self.speed
        self.start = current
        self.real_start = real_current
        return self.speed

    def get_time(self, current: datetime = None) -> datetime:
        if self.paused:
            return self.paused_time
        if current is None:
            current = datetime.now()
        return self.start + (current - self.real_start) * self.speed

    def pause(self) -> bool:
        if not self.paused:
            self.paused_time = self.get_time()
            self.paused = True
            return True
        return False

    def resume(self) -> bool:
        if self.paused:
            self.real_start = datetime.now()
            self.start = self.paused_time
            self.paused = False
            return True
        return False

    def __str__(self) -> str:
        current = self.get_time()
        real_current = datetime.now()
        return "[Clock]" \
               + "\n---------------------" \
               + "\n|      Initial Time : " + str(self.start) \
               + "\n| Initial Real Time : " + str(self.real_start) \
               + "\n|            Offset : " + str(self.start - self.real_start) \
               + "\n|             Speed : " + str(self.speed) \
               + "\n|      CURRENT TIME : " + str(current) \
               + "\n| Current Real Time : " + str(real_current) \
               + "\n---------------------"