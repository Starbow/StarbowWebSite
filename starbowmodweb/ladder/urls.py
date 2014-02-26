from django.conf.urls import patterns, url

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.ladder.views',
    url(r'^$', 'show_ladders'),
    url(r'player/([0-9]+)', 'show_player'),
    url(r'crashreport$', 'crash_report'),
    url(r'(NA|na|EU|eu|KR|kr)', 'show_region'),
)
