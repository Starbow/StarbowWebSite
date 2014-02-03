import os
import json
import binascii
import subprocess

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from starbowmodweb.user.forms import RegistrationForm
from starbowmodweb.user.models import User
from starbowmodweb.ladder.models import Client
from django.conf import settings


def create_forum_account(user, password):
    """ Takes email address and username; returns a uid """
    if settings.MYBB_BRIDGE_PATH:
        cmd = ['php', settings.MYBB_BRIDGE_PATH, user.email, user.username, password]
        output = subprocess.check_output(cmd)
        data = json.loads(output.decode('utf8'))
        if data['status'] == 'failure':
            # Alert the administrators
            return None
        else:
            profile = user.profile
            profile.mybb_uid = data['data']['uid']
            profile.save()


def create_ladder_account(user, authtoken):
    client = Client()
    client.user = user
    client.username = user.username
    client.authkey = authtoken
    client.rating_mean = 25.0
    client.rating_stddev = 25.0/3
    client.ladder_points = 100
    client.ladder_search_radius = 1
    client.total_queue_time = 0
    client.wins = 0
    client.losses = 0
    client.save()


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = binascii.b2a_hex(os.urandom(15))
            authtoken = binascii.b2a_hex(os.urandom(15))
            user = User.objects.create_user(username, email, password)
            create_forum_account(user, password)
            create_ladder_account(user, authtoken)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return HttpResponseRedirect(reverse(user_home))
    else:
        form = RegistrationForm()

    return render(request, 'register.html', dict(form=form))


@login_required
def user_home(request):
    return render(request, 'home.html')
