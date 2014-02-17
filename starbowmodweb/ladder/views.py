from django.shortcuts import render
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import Client, Map, BATTLENET_REGION_NA


def show_ladder(request):
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=50)
    return render(request, 'ladder_home.html', dict(ladder_stats=ladder_na))


def show_player(request, client_id):
    client_id = int(client_id)
    try:
        client = Client.objects.select_related().get(pk=client_id)
        return render(request, 'ladder/player.html', dict(client=client))
    except Client.DoesNotExist:
        return render(request, 'ladder/player_not_found.html', dict(client_id=client_id))


def show_region_stats(request, client_id, region):
    pass


def show_map(request, map_id):
    map = Map.objects.get(pk=map_id)
    return render(request, 'ladder/map.html', dict(map=map))
