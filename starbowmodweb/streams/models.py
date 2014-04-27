from django.db import models
from starbowmodweb.user.models import User
from django.utils.timezone import now

CACHE_INTERVAL = 300


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    url_format = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def needs_update(self):
        return (now() - self.last_update).total_seconds() > CACHE_INTERVAL

    def update_time(self):
        self.last_update = now()


class StreamInfo(models.Model):
    user = models.OneToOneField(User)
    channel_name = models.CharField(max_length=25)
    streaming_platform = models.ForeignKey(StreamingPlatform)
    description = models.TextField(blank=True)
    viewers = models.IntegerField(default=0)
    online = models.BooleanField(default=False)

    def get_url(self):
        return self.streaming_platform.url_format % (self.channel_name,)

    def __unicode__(self):
        return self.channel_name