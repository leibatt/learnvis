import datetime
import datetime as dt
from dateutil import parser
import numpy as np

year_threshold = 1800
default_date = dt.datetime(1000,1,1)

'''
date casting function for strings
'''
def get_date(s):
    date = convert_to_date(s)
    if date is None:
        raise Exception("could not parse as valid date")

def convert_vector_to_dates(v):
    default = default_date#dt.datetime.now()
    def f(s):
        try:
            date = parser.parse(s,fuzzy=True,default=default)
        except Exception as e: # didn't work
           date = default
        return date
    vf = np.vectorize(f,otypes=[np.datetime64])
    result = vf(v)
    return result

def convert_to_date(s):
    try:
        date = parser.parse(s,fuzzy=True,default=default_date)
        if not within_same_hour(date):
            if date.year <= dt.datetime.now().year:
                if date.year >= year_threshold:
                    return date
    except Exception as e: # didn't work
       pass
    return None

def within_same_hour(date):
    now = dt.datetime.now()
    chour = now.hour
    return now.date() == date.date() and date.hour == now.hour

class mydate():
    def __init__(self,s):
        self.date = get_date(s)


