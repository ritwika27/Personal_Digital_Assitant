from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    SCHEDULER=0
    WEB=1
    WEATHERMAN=2
    NAVIGATOR=3
    TIMEKEEPER=4
