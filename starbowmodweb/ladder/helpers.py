from starbowmodweb.ladder.models import ClientRegionStats
from django.db.models import Q


def get_leaderboard(region, offsetby=None, orderby=None, sort=None, count=None):
    query_filter = Q(region=region) & (Q(ladder_wins__gt=0) | Q(ladder_losses__gt=0))
    leaders = ClientRegionStats.objects.select_related().filter(query_filter).order_by(orderby)

    if sort == "DESC":
        leaders = leaders.reverse()

    if count is not None:
        leaders = leaders[:count]

    return leaders
