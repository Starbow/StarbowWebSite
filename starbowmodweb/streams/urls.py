from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.streams.views',
                       url(r'^$', 'list_streams'),
                       url(r'add/$', 'edit_stream'),
)
