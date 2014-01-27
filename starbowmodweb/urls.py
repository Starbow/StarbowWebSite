from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('',
    url(r'^site/', include(patterns('',
        url(r'^browserid/', include('django_browserid.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include('starbowmodweb.site.urls')),
    )))
)
