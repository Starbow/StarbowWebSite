from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.site.views',
    url(r'^$', 'home', name='home'),
    url(r'^about', TemplateView.as_view(template_name='about.html')),
)
