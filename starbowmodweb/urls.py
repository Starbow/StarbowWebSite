from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('starbowmodweb.user.urls')),
    url(r'^ladder/', include('starbowmodweb.ladder.urls')),
    url(r'', include('starbowmodweb.site.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
