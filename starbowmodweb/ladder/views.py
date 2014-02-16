from django.shortcuts import render
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import BATTLENET_REGION_NA


def show_ladder(request):
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=50)
    return render(request, 'ladder_home.html', dict(ladder_stats=ladder_na))
