from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    SCHEDULER=0
    WEB=2
    WEATHERMAN=1
    NAVIGATOR=3
    TIMEKEEPER=4
