from django.http import HttpResponse
from django.shortcuts import render
from django.db import connections

import bbcode


def bbcode_img(tag_name, value, options, parent, context):
    if tag_name in options and 'x' in options[tag_name]:
        options['width'], options['height'] = options[tag_name].split('x', 1)
        del options[tag_name]
    attrs = ' '.join([name+'="{}"' for name in options.keys()])
    return ('<img src="{}" '+attrs+' />').format(value, *options.values())

bbcode_parser = bbcode.Parser()
bbcode_parser.add_formatter("img", bbcode_img, replace_links=False)


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
    for article in articles:

        article['html'] = bbcode_parser.format(article['message'])

    return render(request, 'news_listing.html', dict(articles=articles))
