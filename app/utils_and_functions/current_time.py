import datetime, pytz

def current_time(accuracy="seconds"):
    t = datetime.datetime.now(pytz.timezone('Europe/Moscow')) # current Moscow time
    tm = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond) # aware to naive datetime (with tzinfo == None)

    if accuracy == "microseconds":
        return tm
    tm -= datetime.timedelta(microseconds=tm.microsecond)
    if accuracy == "seconds":
        return tm
    tm -= datetime.timedelta(seconds=tm.second)
    if accuracy == "minutes":
        return tm
    tm -= datetime.timedelta(minutes=tm.minute)
    if accuracy == "hours":
        return tm
    tm -= datetime.timedelta(hours=tm.hour)
    if accuracy == "days":
        return tm
    tm -= datetime.timedelta(days=tm.day)
    if accuracy == "months":
        return tm
    tm -= datetime.timedelta(months=tm.month)
    if accuracy == "years":
        return tm
    tm -= datetime.timedelta(years=tm.year)
    return None