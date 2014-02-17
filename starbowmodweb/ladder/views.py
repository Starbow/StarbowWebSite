from django.shortcuts import render
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import Client, Map, BATTLENET_REGION_NA


def show_ladder(request):
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=50)
    return render(request, 'ladder_home.html', dict(ladder_stats=ladder_na))


def show_player(request, client_id):
    client = Client.objects.get(pk=client_id)
    return render(request, 'ladder/player.html', dict(client=client))


def show_map(request, map_id):
    map = Map.objects.get(pk=map_id)
    return render(request, 'ladder/map.html', dict(map=map))
