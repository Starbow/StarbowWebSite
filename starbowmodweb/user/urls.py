from django.conf.urls import patterns, include, url


# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.user.views',
    url(r'^home', 'user_home', name='user_home'),
)
