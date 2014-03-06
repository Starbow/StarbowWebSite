from django.db import connections
import phpserialize
from dateutil import rrule, relativedelta
from datetime import datetime, timedelta
from starbowmodweb import utils

import logging
logger = logging.getLogger(__name__)


def get_thread(thread_id):
    cursor = connections['mybb'].cursor()
    cursor.execute("SELECT * FROM mybb_threads, mybb_posts WHERE mybb_threads.firstpost = mybb_posts.pid AND mybb_threads.tid=%s", [thread_id])
    thread = utils.dictfetchall(cursor)[0]
    thread['edittime'] = datetime.fromtimestamp(thread['edittime'])
    thread['url'] = "/forum/showthread.php?tid={}".format(thread['tid'])
    return thread


def get_threads(thread_prefix=None, forum_name=None, orderby=None, sort=None, offsetby=None, count=None):
    """ Returns a list of threads from the indicated forumId """
    params = []
    order, limit = "", ""
    tables = ["mybb_threads", "mybb_posts"]
    conditions = [
        "mybb_threads.firstpost = mybb_posts.pid",
        "mybb_threads.visible=1"
    ]

    if forum_name is not None:
        tables.append("mybb_forums")
        conditions.append("mybb_threads.fid = mybb_forums.fid")
        if isinstance(forum_name, basestring):
            conditions.append("mybb_forums.name = %s")
            params.append(forum_name)
        else:
            inClause = ", ".join(["%s"]*len(forum_name))
            conditions.append("mybb_forums.name IN ("+inClause+")")
            params.extend(forum_name)

    if thread_prefix is not None:
        tables.append("mybb_threadprefixes")
        conditions.extend([
            "mybb_threads.prefix = mybb_threadprefixes.pid",
            "mybb_threadprefixes.prefix = %s"
        ])
        params.append(thread_prefix)

    if orderby:
        order = "ORDER BY {}".format(orderby)

    if sort:
        order += " {}".format(sort)

    if count:
        limit = "LIMIT %s"
        params.append(count)

    if offsetby:
        limit += " OFFSET %s"
        params.append(offsetby)

    query_template = "SELECT * FROM {} WHERE {} {} {}"
    query = query_template.format(', '.join(tables), ' AND '.join(conditions), order, limit)
    cursor = connections['mybb'].cursor()

    cursor.execute(query, params)
    threads = utils.dictfetchall(cursor)
    for thread in threads:
        thread['url'] = "/forum/showthread.php?tid={}".format(thread['tid'])
    return threads


def get_events_in_range(calendar_name, start_range, end_range):
    """ Returns an ordered list of events that fall within the specified time range.

        TODO: Adjust times based on encoded timezone
    """
    # Get all of the events that might fall in this time range from the mybb db
    query = '''
        SELECT mybb_events.*
        FROM mybb_events, mybb_calendars
        WHERE mybb_calendars.name = %s
          AND mybb_events.cid = mybb_calendars.cid
          AND (
            (endtime = 0 AND starttime > UNIX_TIMESTAMP(%s))
            OR endtime > UNIX_TIMESTAMP(%s)
          )
    '''
    cursor = connections['mybb'].cursor()
    cursor.execute(query, [calendar_name, start_range, start_range])

    # Iterate over the event listings and expand any repeated or multiday events
    events = list()
    for result in utils.dictfetchall(cursor):
        # myBB records start and end times in unix epoch time
        start_time = datetime.fromtimestamp(result['starttime'])
        end_time = datetime.fromtimestamp(result['endtime'])

        # Figure out the event duration by subtracting the time of day. If duration
        # is negative, assume duration of less than 24 hours so make math easy. Duration
        # is ignored for non-repeating ranged events so this shouldn't be an issue.
        seconds = (result['endtime'] % 86400) - (result['starttime'] % 86400)
        if seconds < 0:
            seconds += 86400
        duration = timedelta(seconds=seconds)

        # Load the repeat data and find all relevant event times
        repeat_data = phpserialize.loads(result['repeats']) if result['repeats'] else None
        times = get_event_times(start_time, min(end_time, end_range), duration, repeat_data)

        # For every time block in the requested range associated with this event
        # copy the results output and insert some useful start and end times
        for (start, end) in filter(lambda (start, end): end >= start_range, times):
            event = result.copy()
            event['start'] = start
            event['end'] = end
            event['url'] = "/forum/calendar.php?action=event&eid={}".format(event['eid'])
            event['is_today'] = datetime.today().date() == start.date()
            events.append(event)

    # Sort chronologically before sending to the screen
    return sorted(events, key=lambda event: event['start'])


def get_event_times(start_time, end_time, duration, repeats):
    """ Applies the given repeat parameters to create a set of event times.

        I couldn't find any offical documentation on the storage format so I had to
        work out behavior of repeat parameters through experimentation and inspection
        of the SQL records that were produced.
    """
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
        start_times = rrule.rrule(rrule.DAILY, interval=interval, dtstart=start_time, until=end_time)
        times = [(start, start+duration) for start in start_times]

    elif repeats['repeats'] == 2:
        # Weekdays, every Monday-Friday
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
