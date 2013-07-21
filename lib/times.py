import datetime
import re
import math
import time

def timestamp_to_string(timestamp, format):
    date = datetime.datetime.fromtimestamp(timestamp)
    return good_strftime(date, format)