from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('',
    url(r'^site/', include(patterns('',
        # Examples:
        # url(r'^$', 'starbowmodweb.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )))
)
