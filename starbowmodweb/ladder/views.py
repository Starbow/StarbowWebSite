from django.shortcuts import render
from django import db
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from starbowmodweb.ladder.forms import CrashReportForm, CrashReport
from starbowmodweb.ladder.helpers import get_matchhistory
from starbowmodweb.ladder.models import Client, REGION_LOOKUP
from starbowmodweb import utils
from datetime import datetime, timedelta
import json


def show_player(request, client_id):
    client_id = int(client_id)
    matches = get_matchhistory(client_id)
    try:
        client = Client.objects.select_related().get(pk=client_id)
        return render(request, 'ladder/player.html', dict(client=client, matches=matches))
    except Client.DoesNotExist:
        return render(request, 'ladder/player_not_found.html', dict(client_id=client_id))


@login_required
def crash_report(request):
    if request.method == 'POST':
        report = CrashReport(user=request.user)
        form = CrashReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return render(request, 'ladder/crash_report_success.html', dict(report=report))
    else:
        form = CrashReportForm()

    return render(request, 'ladder/crash_report_submit.html', dict(form=form))


class LeaderboardDatatable(utils.DatatableQuery):
    COLUMN_LOOKUP = dict(
        username='stats.username',
        rank='rank',
        division='division',
        clientid="clients.id as clientid",
        ladder_points='stats.ladder_points',
        ladder_wins='(stats.ladder_wins-stats.ladder_walkovers) as ladder_wins',
        ladder_losses='(stats.ladder_losses-stats.ladder_forefeits) as ladder_losses',
        ladder_forfeits='stats.ladder_forefeits as ladder_forfeits',
        ladder_walkovers='stats.ladder_walkovers',
    )

    def tables(self, params):
        if 'region' in self.args:
            params.append(int(self.args['region']))
            return """(SELECT (@rank:=@rank+1) as rank, tmp.* FROM (
                           SELECT divisions.name as division, client_region_stats.*
                           FROM client_region_stats, divisions
                           WHERE region = %s
                             AND division_id = divisions.id
                             AND placement_matches_remaining = 0
                           ORDER BY divisions.ladder_group DESC, ladder_points DESC) as tmp
                       ) as stats, clients"""
        else:
            return """(SELECT (@rank:=@rank+1) as rank, tmp.* FROM (
                           SELECT divisions.name as division, clients.id as client_id, clients.*
                           FROM clients, divisions
                           WHERE division_id = divisions.id
                             AND placement_matches_remaining = 0
                           ORDER BY divisions.ladder_group DESC, ladder_points DESC) as tmp
                       ) as stats, clients"""

    def where(self, params):
        return "stats.client_id = clients.id"

    def execute(self, cursor):
        cursor.execute("SET @rank:=0")
        return utils.DatatableQuery.execute(self, cursor)


def datatable_leaderboard(request):
    cursor = db.connection.cursor()
    data = LeaderboardDatatable(request.GET).execute(cursor)
    return HttpResponse(json.dumps(data), mimetype='application/json')


def show_global(request):
    start_date = datetime.utcnow()-timedelta(seconds=7*86400)
    cursor = db.connection.cursor()
    global_stats_query = """
        select sum(race='zerg')/count(*) as zerg,
               sum(race='protoss')/count(*) as protoss,
               sum(race='terran')/count(*) as terran,
               count(distinct matchid) as matches,
               count(distinct clientid) as players
        from match_result_players, match_results
        where match_results.id=matchid
          AND FROM_UNIXTIME(datetime) > %s
    """
    cursor.execute(global_stats_query, [start_date])
    global_stats = utils.dictfetchall(cursor)[0]
    return render(request, 'ladder/global.html', dict(global_stats=global_stats))



def show_region(request, region):
    region_id = REGION_LOOKUP[region.upper()]
    start_date = datetime.utcnow()-timedelta(seconds=7*86400)

    cursor = db.connection.cursor()
    region_stats_query = """
        select sum(race='zerg')/count(*) as zerg,
               sum(race='protoss')/count(*) as protoss,
               sum(race='terran')/count(*) as terran,
               count(distinct matchid) as matches,
               count(distinct clientid) as players
        from match_result_players, match_results
        where match_results.id=matchid
          AND region=%s
          AND FROM_UNIXTIME(datetime) > %s
    """
    cursor.execute(region_stats_query, [region_id, start_date])
    region_stats = utils.dictfetchall(cursor)[0]
    return render(request, 'ladder/region.html', dict(region_str=region.upper(), region=REGION_LOOKUP[region.upper()], region_stats=region_stats))
