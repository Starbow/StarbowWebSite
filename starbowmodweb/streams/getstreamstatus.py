import json
import httplib
from django.core.exceptions import ObjectDoesNotExist
from urllib import urlencode
from starbowmodweb.streams.models import *
from starbowmodweb.config import TWITCH_CLIENT_ID


TWITCH_VERSION = ".v2"
TWITCH_QRY_LIMIT = 100


def update_stream_cache():
    try:
        platform = StreamingPlatform.objects.get(name='Twitch')
        channels = StreamInfo.objects.filter(streaming_platform=platform)

        update_twitch_stream_cache(channels)

        # update last update
        platform.update_time()
        platform.save()
    except ObjectDoesNotExist:
        pass


def update_twitch_stream_cache(channels):
    online_streams = dict()

    # slice requests because there is a limit of how many channels
    # can be queried per request
    channels_slice = channels
    while len(channels_slice) > 0:
        qry_channels = channels_slice[:TWITCH_QRY_LIMIT]
        qry_channels = map(lambda x: x.channel_name, qry_channels)

        for stream in get_twitch_online_streams(qry_channels):
            try:
                online_streams[stream['channel']['name']] = stream
            except (KeyError, TypeError):
                pass

        channels_slice = channels_slice[TWITCH_QRY_LIMIT:]

    # Put into cache
    for stream in channels:
        online_info = online_streams.get(stream.channel_name, None)
        if online_info is not None:
            # stream is in reply -> online
            stream.online = True
            try:
                stream.viewers = online_info['viewers']
            except (KeyError, TypeError):
                pass
        else:
            # stream is not in reply -> offline
            stream.online = False
            stream.viewers = 0

        stream.save()


def twitch_request(action, params):
    conn = httplib.HTTPSConnection("api.twitch.tv")

    params = urlencode(params)
    accept_value = "application/vnd.twitchtv%s+json" % (TWITCH_VERSION,)

    # request
    conn.request("GET", "/kraken/%s/?%s" % (action, params),
                 headers={"Accept": accept_value,
                          "Client-ID:": TWITCH_CLIENT_ID})

    # response
    response = conn.getresponse()
    data = response.read().decode("utf-8", errors='ignore')
    conn.close()
    data = json.loads(data)
    return data


def get_twitch_online_streams(channels):
    try:
        # form url
        channels_csv = ",".join(channels)
        params = [
            ("channel", channels_csv),
            ("limit", TWITCH_QRY_LIMIT)
        ]

        data = twitch_request('streams', params)
        streams = data['streams']

        return streams
    except (httplib.HTTPException, ValueError, KeyError, TypeError):
        return []


def twitch_channel_exists(channel):
    try:
        # form url
        params = []

        data = twitch_request('channels/' + channel, params)
        return data['name'] == channel
    except (httplib.HTTPException, ValueError, KeyError, TypeError):
        return False