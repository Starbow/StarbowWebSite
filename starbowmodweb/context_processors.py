from datetime import datetime, timedelta

from django.conf import settings
from starbowmodweb import mybb


def starbowmodweb(request):
    now = datetime.now()
    later = now+timedelta(seconds=30*86400)
    return dict(
        ABOUT_PAGES=settings.ABOUT_PAGES,
        recent_articles=mybb.get_threads(forum_name="News and Announcements", orderby="mybb_threads.dateline", sort="DESC", count=7),
        upcoming_events=mybb.get_events_in_range("Default Calendar", now, later)[:7],
    )
