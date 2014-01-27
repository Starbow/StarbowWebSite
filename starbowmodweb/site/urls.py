from django.conf.urls import patterns, include, url

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.site.views',
    url(r'', 'home', name='home')
)
