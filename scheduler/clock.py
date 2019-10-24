from datetime import datetime, timedelta
import copy


class Clock:
    init_start: datetime = None
    init_speed: float = 1

    start: datetime = None
    paused: bool = False
    rate: int = 1  # loop rate in seconds
    speed: float = 1
    elapsed: float = 0 # number of seconds elapsed

    def __init__(self, start_time: datetime = datetime(2019, 1, 7, 1), speed: float = 1) -> None:
        self.init_start = copy.deepcopy(start_time)
        self.init_speed = speed if speed > 0 else 1
        self.start = start_time
        self.speed = self.init_speed

    def reset(self):
        self.start = self.init_start
        self.speed = self.init_speed

    def set_speed(self, speed: float) -> float:
        self.speed = speed if speed > 0 else self.speed
        self.start = self.get_time()
        self.elapsed = 0
        return self.speed

    def get_time(self) -> datetime:
        return self.start + timedelta(seconds=self.elapsed)

    def next(self) -> None:
        self.elapsed += self.rate * self.speed

    def pause(self) -> bool:
        if not self.paused:
            self.paused = True
            return True
        return False

    def resume(self) -> bool:
        if self.paused:
            self.paused = False
            return True
        return False

    def __str__(self) -> str:
        current = self.get_time()
        real_current = datetime.now()
        return "[Clock]" \
               + "\n---------------------" \
               + "\n|      Initial Time : " + str(self.start) \
               + "\n|             Speed : " + str(self.speed) \
               + "\n|      CURRENT TIME : " + str(current) \
               + "\n---------------------"
