from django.shortcuts import render
from starbowmodweb.ladder.helpers import get_leaderboard
from starbowmodweb.ladder.models import Client, Map, MatchResult, BATTLENET_REGION_NA, BATTLENET_REGION_EU


def show_ladders(request):
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=50)
    ladder_eu = get_leaderboard(region=BATTLENET_REGION_EU, orderby='ladder_points', sort="DESC", count=50)
    return render(request, 'ladder_home.html', dict(ladder_na=ladder_na, ladder_eu=ladder_eu))


def show_player(request, client_id):
    client_id = int(client_id)
    matches = MatchResult.objects.select_related().filter(players__client_id=client_id)
    try:
        client = Client.objects.select_related().get(pk=client_id)
        return render(request, 'ladder/player.html', dict(client=client, matches=matches))
    except Client.DoesNotExist:
        return render(request, 'ladder/player_not_found.html', dict(client_id=client_id))


def show_map(request, map_id):
    map = Map.objects.get(pk=map_id)
    return render(request, 'ladder/map.html', dict(map=map))
