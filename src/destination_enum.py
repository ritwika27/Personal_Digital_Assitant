from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    SCHEDULER=0
    WEATHERMAN=1
    NAVIGATOR=2
    TIMEKEEPER=3
    WEB=4
