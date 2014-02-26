from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from starbowmodweb.ladder.forms import CrashReportForm, CrashReport
from starbowmodweb.ladder.helpers import get_leaderboard, get_matchhistory
from starbowmodweb.ladder.models import Client, BATTLENET_REGION_NA, BATTLENET_REGION_EU


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


def show_region(request, region):
    return render(request, 'ladder/region.html')
