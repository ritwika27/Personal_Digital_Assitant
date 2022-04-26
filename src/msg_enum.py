from enum import IntEnum, unique

@unique
class Msg_type(IntEnum):
    NEW_EVENT=0
    INITIALIZED=1
    UPDATE_ESTIMATE=2
    STATUS=3
    UPDATE_WEATHER=4

    CURR_WEATHER=5 # for demo

