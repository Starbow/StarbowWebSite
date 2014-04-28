from starbowmodweb.ladder.models import ClientRegionStats, MatchResult
from django.db.models import Q
from datetime import datetime


def get_leaderboard(region, offsetby=None, orderby=None, sort=None, count=None):
    query_filter = Q(region=region) & (Q(ladder_wins__gt=0) | Q(ladder_losses__gt=0))
    leaders = ClientRegionStats.objects.select_related().filter(query_filter).order_by(*orderby)

    if sort == "DESC":
        leaders = leaders.reverse()

    if count is not None:
        leaders = leaders[:count]

    return leaders


def get_matchhistory(client_id):
    matches = list()
    raw_matches = MatchResult.objects.select_related('MatchmakerMatch', 'MatchResultPlayer', 'MatchResultPlayer__Client').filter(players__client_id=client_id).order_by('datetime').reverse()
    for raw_match in raw_matches:
        match = {
            'id': raw_match.pk,
            'mm_id': raw_match.matchmaker_match_id,
            'datetime': datetime.fromtimestamp(raw_match.datetime),
            'region': raw_match.get_region_display(),
            'map_name': raw_match.map.bnet_name.replace('Starbow - ', ''),
        }
        raw_players = raw_match.players
        for raw_player in raw_players.all():
            if raw_player.client.pk == client_id:
                if raw_player.race.lower() == 'forfeit':
                    match['result'] = 'Forfeit'
                elif raw_player.race.lower() == 'walkover':
                    match['result'] = 'Walkover'
                elif raw_player.victory:
                    match['result'] = 'Victory'
                else:
                    match['result'] = 'Defeat'

                match['point_difference'] = raw_player.point_difference
                if match['point_difference'] > 0:
                    match['point_difference'] = "+{}".format(match['point_difference'])
                match['player1'] = raw_player
            else:
                match['player2'] = raw_player

            if raw_player.race:
                    raw_player.race_icon = '/static/ladder/img/'+raw_player.race.lower()+".png"

        matches.append(match)
    return matches
