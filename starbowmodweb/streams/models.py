from django.db import models
from starbowmodweb.user.models import User
from django.utils.timezone import now


class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    url_format = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def update_time(self):
        self.last_update = now()


class StreamInfo(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    channel_name = models.CharField(max_length=25)
    streaming_platform = models.ForeignKey(StreamingPlatform)
    description = models.CharField(max_length=80, blank=True)
    viewers = models.IntegerField(default=0)
    online = models.BooleanField(default=False)

    def get_url(self):
        return self.streaming_platform.url_format % (self.channel_name,)

    def get_channel_name(self):
        return self.user.username if self.user else self.channel_name

    def __unicode__(self):
        return self.channel_name