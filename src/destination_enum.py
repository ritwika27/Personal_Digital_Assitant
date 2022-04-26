from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    SCHEDULER=0
    WEATHERMAN=1
    WEB=2
    NAVIGATOR=3
    TIMEKEEPER=4
