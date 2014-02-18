from django.shortcuts import render
from datetime import datetime, timedelta
from starbowmodweb import mybb
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import BATTLENET_REGION_NA, BATTLENET_REGION_EU, BATTLENET_REGION_KR


def home(request):
    now = datetime.now()
    later = now+timedelta(seconds=30*86400)
    upcoming_events = mybb.get_events_in_range("Default Calendar", now, later)[:7]
    latest_article = mybb.get_threads(forum_name="News and Announcements", count=1, orderby="mybb_threads.dateline", sort="DESC")[0]
    recent_articles = mybb.get_threads(forum_name="News and Announcements", count=7, offsetby=1, orderby="mybb_threads.dateline", sort="DESC")
    recent_discussions = mybb.get_threads(thread_prefix="Discussion", count=7, orderby="mybb_threads.dateline", sort="DESC")

    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=10)
    ladder_eu = get_leaderboard(region=BATTLENET_REGION_EU, orderby='ladder_points', sort="DESC", count=10)
    ladder_kr = get_leaderboard(region=BATTLENET_REGION_KR, orderby='ladder_points', sort="DESC", count=10)
    return render(request, 'site_home.html', dict(
        upcoming_events=upcoming_events,
        latest_article=latest_article,
        recent_articles=recent_articles,
        recent_discussions=recent_discussions,
        ladder_na=ladder_na,
        ladder_eu=ladder_eu,
        ladder_kr=ladder_kr,
    ))


def view_news(request):
    articles = mybb.get_threads(forum_name="News and Announcements", sort="DESC")
    return render(request, 'news.html', dict(articles=articles))


def view_calendar(request):
    now = datetime.now()
    later = now+timedelta(seconds=30*86400)
    events = mybb.get_events_in_range("Default Calendar", now, later)
    return render(request, 'calendar.html', dict(events=events))
