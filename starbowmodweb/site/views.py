from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta
from starbowmodweb import mybb
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import BATTLENET_REGION_NA, BATTLENET_REGION_EU, BATTLENET_REGION_KR


def home(request):
    recent_discussions = mybb.get_threads(forum_name=settings.DISCUSSION_FORUMS, count=7, orderby="mybb_threads.dateline", sort="DESC")
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=10)
    ladder_eu = get_leaderboard(region=BATTLENET_REGION_EU, orderby='ladder_points', sort="DESC", count=10)
    ladder_kr = get_leaderboard(region=BATTLENET_REGION_KR, orderby='ladder_points', sort="DESC", count=10)
    return render(request, 'site_home.html', dict(
        recent_discussions=recent_discussions,
        ladder_na=ladder_na,
        ladder_eu=ladder_eu,
        ladder_kr=ladder_kr,
    ))


def view_streams(request):
    return render(request, 'streams.html')


def view_news(request):
    articles = mybb.get_threads(forum_name="News and Announcements", orderby="mybb_threads.dateline", sort="DESC")
    return render(request, 'news.html', dict(articles=articles))


def view_events(request):
    now = datetime.utcnow()
    later = now + timedelta(seconds=30*86400)
    events = mybb.get_events_in_range("Default Calendar", now, later)
    return render(request, 'events.html', dict(events=events))


def about_page(request, name):
    name = name.lower() or 'overview'
    if name not in settings.ABOUT_PAGES:
        raise Http404
    return render(request, 'thread_page.html', dict(thread=mybb.get_thread(settings.ABOUT_PAGES[name][1])))
