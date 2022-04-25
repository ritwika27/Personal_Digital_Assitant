from enum import IntEnum, unique

@unique
class Msg_type(IntEnum):
    NEW_LOCATION=0
    INITIALIZED=1
    CURR_WEATHER=2
    UPDATE_ESTIMATE=3
