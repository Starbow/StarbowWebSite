import os
import json
import binascii
import subprocess

from django.db import connections
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from starbowmodweb.user.forms import RegistrationForm
from starbowmodweb.user.models import User
from django.conf import settings
from django.db import transaction
from starbowmodweb import utils

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MyBBError(Exception):
    pass


def sync_users():
    cursor = connections['mybb'].cursor()
    cursor.execute("SELECT uid, username, loginkey, email FROM mybb_users")
    users = utils.dictfetchall(cursor)

    for mybb_user in users:
        try:
            User.objects.get(email=mybb_user['email'])
            print("Found {}".format(mybb_user['email']))
        except User.DoesNotExist:
            print("Creating {}".format(mybb_user['email']))
            password = binascii.b2a_hex(os.urandom(15))
            User.objects.create_user(mybb_user['username'], mybb_user['email'], password)


def create_forum_account(user, password):
    """ Takes email address and username; returns a uid """
    if settings.MYBB_BRIDGE_PATH:
        cmd = ['php', settings.MYBB_BRIDGE_PATH, user.email, user.username, password]
        output = subprocess.check_output(cmd)
        return json.loads(output.decode('utf8'))


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = binascii.b2a_hex(os.urandom(15))

            try:
                with transaction.atomic():
                    user = User.objects.create_user(username, email, password)
                    forum_data = create_forum_account(user, password)
                    if forum_data['status'] == 'failure':
                        raise MyBBError(forum_data['data'])
                    else:
                        profile = user.profile
                        profile.mybb_uid = forum_data['data']['uid']
                        profile.mybb_loginkey = forum_data['data']['loginkey']
                        profile.save()
                        return render(request, 'user/register_success.html', dict(
                            email=email,
                            username=username
                        ))
            except MyBBError as e:
                # Alert the administrators
                logger.error("MyBB account creation failure: {}".format(e))
                return render(request, 'user/register_failure.html', dict(
                    email=email,
                    username=username,
                    messages=str(e),
                ))

    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', dict(form=form))


@login_required
def user_home(request):
    return render(request, 'user/home.html', dict(CLIENT_URLS=settings.CLIENT_URLS))
