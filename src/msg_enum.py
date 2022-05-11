from enum import IntEnum, unique

@unique
class Msg_type(IntEnum):
    NEW_EVENT=0
    DELETE_EVENT=1
    INITIALIZED=2
    STATUS=3

    UPDATE_EVENT_WEATHER=4
    UPDATE_CURRENT_WEATHER=5
    UPDATE_ESTIMATE=6
    WEATHER_NOTIFICATION=7
    RESPONSE_ESTIMATE=8

    UPDATE_USER_LOCATION=9
    REQUEST_ESTIMATE=10
    REQUEST_WEATHER=11




