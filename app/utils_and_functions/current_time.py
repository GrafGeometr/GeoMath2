import datetime, pytz

def current_time():
    t = datetime.datetime.now(pytz.timezone('Europe/Moscow')) # current Moscow time
    tm = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond) # aware to naive datetime (with tzinfo == None)
    tm = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
    return tm