from django.shortcuts import render, render_to_response
from django.db import connections
import phpserialize
from dateutil import rrule, relativedelta
from datetime import datetime, timedelta


def home(request):
    return render(request, 'base.html')


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_event_times(start_time, end_time, duration, repeats):
    if repeats is None:
        # Single day, all day event
        end_time = start_time + relativedelta.relativedelta(hours=24)
        times = [(start_time, end_time)]

    elif repeats['repeats'] == 0:
        # Single event, time range
        times = [(start_time, end_time)]

    elif repeats['repeats'] == 1:
        # Repeats daily every X days
        interval = repeats['days']
        print(dict(interval=interval, dtstart=start_time, until=end_time))
        start_times = rrule.rrule(rrule.DAILY, interval=interval, dtstart=start_time, until=end_time)
        times = [(start, start+duration) for start in start_times]

    elif repeats['repeats'] == 2:
        # Weekdays
        days = [0, 1, 2, 3, 4]
        start_times = rrule.rrule(rrule.WEEKLY, byweekday=days, dtstart=start_time, until=end_time)
        times = [(start, start+duration) for start in start_times]

    elif repeats['repeats'] == 3:
        # Weekly on certain days every X weeks
        interval = repeats['weeks']
        # myBB uses 0 for Sunday, transform into 0 for Monday
        days = [(day + 6) % 7 for day in repeats['days'].values()]
        start_times = rrule.rrule(rrule.WEEKLY, interval=interval, byweekday=days, dtstart=start_time, until=end_time)
        times = [(start, start+duration) for start in start_times]

    elif repeats['repeats'] == 4:
        # Monthly on certain days (complicated) every X months
        interval = repeats['months']
        if 'day' in repeats:
            monthday = repeats['day']
            start_times = rrule.rrule(rrule.MONTHLY, interval=interval, bymonthday=monthday, dtstart=start_time, until=end_time)
            times = [(start, start+duration) for start in start_times]
        else:
            bysetpos = repeats['occurance']
            weekday = (repeats['weekday'] + 6) % 7
            start_times = rrule.rrule(rrule.MONTHLY, bysetpos=bysetpos, interval=interval, byweekday=weekday, dtstart=start_time, until=end_time)
            times = [(start, start+duration) for start in start_times]

    elif repeats['repeats'] == 5:
        # Yearly on certain days every X years
        interval = repeats['years']
        if 'day' in repeats:
            monthday = repeats['day']
            month = repeats['month']
            start_times = rrule.rrule(rrule.YEARLY, interval=interval, bymonth=month, bymonthday=monthday, dtstart=start_time, until=end_time)
            times = [(start, start+duration) for start in start_times]
        else:
            bysetpos = repeats['occurance']
            weekday = (repeats['weekday'] + 6) % 7
            month = repeats['month']
            start_times = rrule.rrule(rrule.YEARLY, bysetpos=bysetpos, interval=interval, bymonth=month, byweekday=weekday, dtstart=start_time, until=end_time)
            times = [(start, start+duration) for start in start_times]

    return times


def view_calendar(request):
    NOW = datetime.now()
    EVENT_HORIZON = NOW+relativedelta.relativedelta(days=30)

    cursor = connections['mybb'].cursor()
    cursor.execute("SELECT * FROM mybb_events WHERE (endtime = 0 AND starttime > UNIX_TIMESTAMP(%s)) OR endtime > UNIX_TIMESTAMP(%s)", [NOW, NOW])

    events = list()
    for result in dictfetchall(cursor):
        # Start and end times, if repeat event, these mark the range boundaries.
        start_time = datetime.fromtimestamp(result['starttime'])
        end_time = datetime.fromtimestamp(result['endtime'])
        print(dict(start=start_time, end=end_time))

        # Figure out the event duration, assume less than 24 hours
        seconds = (result['endtime'] % 86400) - (result['starttime'] % 86400)
        if seconds < 0:
            seconds += 86400
        print("Duration: {}".format(seconds))
        duration = timedelta(seconds=seconds)

        # Get the repeats data and figure out our times
        repeats = phpserialize.loads(result['repeats'])
        times = get_event_times(start_time, min(end_time, EVENT_HORIZON), duration, repeats)

        print(result['name'])
        print(times)
        for (start, end) in times:
            if end < NOW:
                continue
            event = result.copy()
            event['start'] = start
            event['end'] = end
            events.append(event)

    # Sort chronologically before sending to the screen
    events.sort(key=lambda event: event['start'])
    return render(request, 'calendar.html', dict(events=events))
