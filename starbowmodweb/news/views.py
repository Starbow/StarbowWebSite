from django.http import HttpResponse
from django.shortcuts import render
from django.db import connections


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def all_news(request):
    cursor = connections['mybb'].cursor()
    cursor.execute("SELECT * FROM mybb_threads JOIN mybb_posts WHERE firstpost=mybb_posts.pid AND mybb_threads.fid=%s AND mybb_threads.visible=1", [3])
    articles = dictfetchall(cursor)
    return render(request, 'news_listing.html', dict(articles=articles))
