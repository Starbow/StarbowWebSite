from django.conf.urls import patterns, url

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.ladder.views',
    url(r'^$', 'show_ladders'),
    url(r'map/([0-9]+)', 'show_map'),
    url(r'player/([0-9]+)', 'show_player'),
)
