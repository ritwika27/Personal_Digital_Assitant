from enum import IntEnum, unique

@unique
class Msg_type(IntEnum):
    NEW_EVENT=0
    INITIALIZED=1
    UPDATE_ESTIMATE=2
    STATUS=3

    CURR_WEATHER=4 # for demo

