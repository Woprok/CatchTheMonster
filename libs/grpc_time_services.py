import datetime
import random

import grpc
from protos.time_pb2 import *
from protos.time_pb2_grpc import *

def time_generate_request():
    rv = TimeRequest()
    rv.Seconds = random.choice([True, False])
    rv.Minutes = random.choice([True, False])
    rv.Hours = random.choice([True, False])
    rv.Day = random.choice([True, False])
    rv.Month = random.choice([True, False])
    rv.Year = random.choice([True, False])
    rv.DayOfWeek = random.choice([True, False])
    rv.DayOfYear = random.choice([True, False])
    rv.IsDaylightSavingTime = random.choice([True, False])
    return rv

def time_generate_response(rq):
    rv = TimeResponse()
    now = datetime.datetime.now()
    if rq.Seconds:
        rv.Seconds = now.second
    if rq.Minutes:
        rv.Minutes = now.minute
    if rq.Hours:
        rv.Hours = now.hour
    if rq.Day:
        rv.Day = now.day
    if rq.Month:
        rv.Month = now.month
    if rq.Year:
        rv.Year = now.year
    if rq.DayOfWeek:
        rv.DayOfWeek = now.timetuple().tm_wday
    if rq.DayOfYear:
        rv.DayOfYear = now.timetuple().tm_yday - 1
    if rq.IsDaylightSavingTime:
        rv.IsDaylightSavingTime = now.timetuple().tm_isdst
    return rv

def time_string(tr):
    return f'Limited time: {tr.Hours}:{tr.Minutes}:{tr.Seconds}-{tr.Day}.{tr.Month}.{tr.Year}-{tr.DayOfWeek}-{tr.DayOfYear}-{tr.IsDaylightSavingTime}'

# Server Service implementation.
# The implementation inherits from a generated base class.
class TimeRequestProviderServerServicer(TimeRequestProviderServicer):
    def RequestTime(self, request, context):
        print("Request", time_string(request))
        response = time_generate_response(request)
        print("Response", time_string(response))
        return response

# Client Message Spamer
def time_send_request(stub):
        request = time_generate_request()
        print("Request", time_string(request))
        # Call the service through the stub object.
        response = stub.RequestTime(request)
        print("Response", time_string(response))