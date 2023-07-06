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

def dt_from_str(dt_str, accuracy="minutes"):
    try:
        if accuracy == "microseconds":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f")
        elif accuracy == "seconds":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
        elif accuracy == "minutes":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
        elif accuracy == "hours":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H")
        elif accuracy == "days":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        elif accuracy == "months":
            dt = datetime.datetime.strptime(dt_str, "%Y-%m")
        elif accuracy == "years":
            dt = datetime.datetime.strptime(dt_str, "%Y")
        else:
            dt = None
        return dt
    except:
        return None
    
def str_from_dt(dt, accuracy="minutes"):
    try:
        if accuracy == "microseconds":
            dt_str = datetime.datetime.strftime(dt, "%d %b %Y, %H:%M:%S.%f")
        elif accuracy == "seconds":
            dt_str = datetime.datetime.strftime(dt, "%d %b %Y, %H:%M:%S")
        elif accuracy == "minutes":
            dt_str = datetime.datetime.strftime(dt, "%d %b %Y, %H:%M")
        elif accuracy == "hours":
            dt_str = datetime.datetime.strftime(dt, "%d %b %Y, %H")
        elif accuracy == "days":
            dt_str = datetime.datetime.strftime(dt, "%d %b %Y")
        elif accuracy == "months":
            dt_str = datetime.datetime.strftime(dt, "%b %Y")
        elif accuracy == "years":
            dt_str = datetime.datetime.strftime(dt, "%Y")
        else:
            dt_str = None
        return dt_str
    except:
        return None