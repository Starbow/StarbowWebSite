from django.shortcuts import render
from datetime import datetime, timedelta
from starbowmodweb import mybb


def home(request):
    return render(request, 'base.html')


def view_news(request):
    articles = mybb.get_threads(3)
    return render(request, 'news.html', dict(articles=articles))


def view_calendar(request):
    NOW = datetime.now()
    EVENT_HORIZON = NOW+timedelta(seconds=30*86400)
    events = mybb.get_events_in_range(NOW, EVENT_HORIZON)
    return render(request, 'calendar.html', dict(events=events))
