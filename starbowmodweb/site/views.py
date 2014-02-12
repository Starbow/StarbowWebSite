from django.shortcuts import render
from datetime import datetime, timedelta
from starbowmodweb import mybb


def home(request):
    now = datetime.now()
    later = now+timedelta(seconds=30*86400)
    upcoming_events = mybb.get_events_in_range("Default Calendar", now, later)[:7]
    recent_articles = mybb.get_threads("News and Announcements", count=7)
    return render(request, 'site_home.html', dict(
        upcoming_events=upcoming_events,
        recent_articles=recent_articles
    ))


def view_news(request):
    articles = mybb.get_threads("News and Announcements")
    return render(request, 'news.html', dict(articles=articles))


def view_calendar(request):
    now = datetime.now()
    later = now+timedelta(seconds=30*86400)
    events = mybb.get_events_in_range("Default Calendar", now, later)
    return render(request, 'calendar.html', dict(events=events))
