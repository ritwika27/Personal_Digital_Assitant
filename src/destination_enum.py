from enum import IntEnum, unique

@unique
class Dest(IntEnum):
    SCHEDULER=0
    TIMEKEEPER=1
    WEATHERMAN=2
    NAVIGATOR=3
    WEB=4
