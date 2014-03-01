from django.shortcuts import render
from django import db
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from starbowmodweb.ladder.forms import CrashReportForm, CrashReport
from starbowmodweb.ladder.helpers import get_leaderboard, get_matchhistory
from starbowmodweb.ladder.models import Client, BATTLENET_REGION_NA, BATTLENET_REGION_EU, REGION_LOOKUP
from starbowmodweb import utils
import json

def show_ladders(request):
    ladder_na = get_leaderboard(region=BATTLENET_REGION_NA, orderby='ladder_points', sort="DESC", count=50)
    ladder_eu = get_leaderboard(region=BATTLENET_REGION_EU, orderby='ladder_points', sort="DESC", count=50)
    return render(request, 'ladder_home.html', dict(ladder_na=ladder_na, ladder_eu=ladder_eu))


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





class DatatableQuery(object):
    """
    Requires additional post args:
        dimensions are used for GROUP BY
        observations are used for selecting columns

    Implement `def where(self, params)` and `def tables(self, params)` to use
    """
    counting_query_template = "SELECT count({}) FROM {} WHERE {} {}"
    filtered_query_template = "SELECT SQL_CALC_FOUND_ROWS {} FROM {} WHERE {} {} {} {} {}"

    def __init__(self, args):
        self.args = args
        self.dimensions = []
        self.observations = []
        if self.args.get('dimensions', False):
            self.dimensions = self.args['dimensions'].split(',')
        if self.args.get('observations', False):
            self.observations = self.args['observations'].split(',')
        self.columns = self.dimensions + self.observations

    def execute(self, cursor):
        # Construct the standard query parts based on the requested dimensions/observations
        groupby, countColumn, countby = "", "*", ""
        if self.dimensions:
            groupby = 'GROUP BY ' + ', '.join(self.dimensions)
            countColumn = 'distinct '+self.dimensions[-1]
            if self.dimensions[:-1]:
                countby = 'GROUP BY ' + ', '.join(self.dimensions[:-1])
        basicParams = list()
        select = ', '.join(self.COLUMN_LOOKUP[column] for column in self.columns)
        tables = self.tables(basicParams)
        where = self.where(basicParams)
        params = list(basicParams)
        orderby = self.orderby(params)
        limitby = self.limitby(params)
        filterby = self.filterby(params)
        # Get the filtered results
        filtered_query = self.filtered_query_template.format(select, tables, where, filterby, groupby, orderby, limitby)
        print(filtered_query)
        print(params)
        cursor.execute(filtered_query, params)
        data = [[row[c] for c in self.columns] for row in utils.dictfetchall(cursor)]
        # Get the total number of filtered rows
        cursor.execute("SELECT FOUND_ROWS()")
        filtered_total = cursor.fetchone()[0]
        # Get the total number of possible results
        counting_query = self.counting_query_template.format(countColumn, tables, where, countby)
        cursor.execute(counting_query, basicParams)
        counting_total = cursor.fetchone()[0]
        # Format the results for datatable's consumptions
        return json.dumps(dict(
            sEcho=int(self.args['sEcho']),
            iTotalRecords=counting_total,
            iTotalDisplayRecords=filtered_total,
            aaData=data
        ))

    def filterby(self, params):
        filterRules = list()
        searchString = self.args.get('sSearch', "")
        if searchString != "":
            for i, columnName in enumerate(self.columns):
                if self.args.get('bSearchable_{}'.format(i), False) == 'true':
                    filterRules.append("{} LIKE %s".format(columnName))
                    params.append('%{}%'.format(searchString))
            if filterRules:
                filterRules = ['({})'.format(' OR '.join(filterRules))]
        for i, columnName in enumerate(self.columns):
            searchable = self.args.get('bSearchable_'.format(i), False) == 'true'
            searchString = self.args.get('sSearch'.format(i), "")
            if searchable and searchString != "":
                filterRules.append("{} LIKE %s".format(columnName))
                params.append('%{}%'.format(searchString))
        filterby = ""
        if filterRules:
            filterby = " AND "+" AND ".join(filterRules)
        return filterby

    def orderby(self, params):
        orderRules = list()
        if 'iSortCol_0' in self.args:
            sortColumnCount = int(self.args['iSortingCols'])
            for i in range(sortColumnCount):
                sortColumn = int(self.args['iSortCol_{}'.format(i)])
                if self.args.get('bSortable_{}'.format(sortColumn), False) == 'true':
                    sortDir = self.args.get('sSortDir_{}'.format(i), 'desc')
                    sortDir = ("ASC" if sortDir == 'asc' else "DESC")
                    rule = "{} {}".format(self.columns[sortColumn], sortDir)
                    orderRules.append(rule)
        orderby = ""
        if orderRules:
            orderby = " ORDER BY "+", ".join(orderRules)
        return orderby

    def limitby(self, params):
        limitby = ""
        if 'iDisplayStart' in self.args and self.args['iDisplayLength'] != "-1":
            offset = int(self.args['iDisplayStart'])
            length = int(self.args['iDisplayLength'])
            limitby = " LIMIT {}, {}".format(offset, length)
        return limitby

    def tables(self, params):
        raise NotImplementedError()

    def where(self, params):
        raise NotImplementedError()


class LeaderboardDatatable(DatatableQuery):
    COLUMN_LOOKUP = dict(
        username='username',
        rank='rank',
        ladder_points='stats.ladder_points',
        ladder_wins='(stats.ladder_wins-stats.ladder_walkovers) as ladder_wins',
        ladder_losses='(stats.ladder_losses-stats.ladder_forefeits) as ladder_losses',
        ladder_forfeits='stats.ladder_forefeits',
        ladder_walkovers='stats.ladder_walkovers',
    )

    def tables(self, params):
        params.append(int(self.args['region']))
        return "(SELECT (@rank:=@rank+1) as rank, client_region_stats.* FROM client_region_stats WHERE region = %s ORDER BY ladder_points DESC) as stats, clients"

    def where(self, params):
        params.append(int(self.args['region']))
        return "stats.client_id = clients.id AND region = %s AND (stats.ladder_wins+stats.ladder_losses) > 0"

    def execute(self, cursor):
        cursor.execute("SET @rank:=0")
        return DatatableQuery.execute(self, cursor)


def datatable_leaderboard(request):
    cursor = db.connection.cursor()
    data = LeaderboardDatatable(request.GET).execute(cursor)
    return HttpResponse(data, mimetype='application/json')


def show_region(request, region):
    return render(request, 'ladder/region.html', dict(region=REGION_LOOKUP[region.upper()]))
