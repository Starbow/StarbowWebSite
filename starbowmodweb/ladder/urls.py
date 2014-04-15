from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# Wrap our patterns in /site/ to match our deployment environment
urlpatterns = patterns('starbowmodweb.ladder.views',
    url(r'^$', TemplateView.as_view(template_name="ladder/old_home.html")),
    url(r'player/([0-9]+)', 'show_player'),
    url(r'crashreport$', 'crash_report'),
    url(r'(NA|na|EU|eu|KR|kr)', 'show_region'),
    url(r'global', 'show_global'),
    url(r'datatable', 'datatable_leaderboard'),
)
