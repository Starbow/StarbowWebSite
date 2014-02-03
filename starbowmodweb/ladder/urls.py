from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.ladder.views',
    url(r'^$', 'show_ladder'),
)
