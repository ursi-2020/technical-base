from datetime import datetime, timedelta

class Clock:

    paused : bool = False
    paused_time : datetime = None
    real_start: datetime = None
    start: datetime = None
    speed: float = 1

    def __init__(self, start_time: datetime = datetime(2019, 1, 7, 1), speed: float = 1) -> None:
        self.real_start = datetime.now()
        self.start = start_time
        self.speed = speed if speed > 0 else 1

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed : float) -> float:
        real_current = datetime.now()
        current = self.get_time(real_current)
        self.speed = speed if speed > 0 else self.speed
        self.start = current
        self.real_start = real_current
        return self.speed

    def get_time(self, current: datetime = None) -> datetime:
        if self.paused:
            return self.paused_time
        if current == None:
            current = datetime.now()
        return self.start + (current - self.real_start) * self.speed

    def pause(self) -> None:
        if not self.paused:
            self.paused_time = self.get_time()
            self.paused = True

    def resume(self) -> None:
        if self.paused:
            self.real_start = datetime.now()
            self.start = self.paused_time
            self.paused = False
    
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

clock : Clock = None