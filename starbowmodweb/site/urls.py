from django.conf.urls import patterns, url

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.site.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/(.*)', 'about_page'),
    url(r'^calendar', 'view_calendar'),
    url(r'^news', 'view_news'),
)
