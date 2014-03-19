from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.site.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/(.*)', 'about_page'),
    url(r'^calendar', RedirectView.as_view(url='events', permanent=True)),
    url(r'^events', 'view_events'),
    url(r'^news', 'view_news'),
    url(r'^streams', 'view_streams'),
)
