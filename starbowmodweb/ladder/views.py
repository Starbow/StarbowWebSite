from django.shortcuts import render
from starbowmodweb.ladder.models import Client


def show_ladder(request):
    query = 'SELECT * FROM ladder_client WHERE wins != 0 OR losses != 0 ORDER BY ladder_points'
    query = 'SELECT * FROM ladder_client'
    clients = Client.objects.raw(query)
    return render(request, 'ladder_home.html', dict(clients=clients))
