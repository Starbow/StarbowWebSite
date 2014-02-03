from django.db import models


class Client(models.Model):
    user = models.ForeignKey('user.User')
    authkey = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=30)
    rating_mean = models.FloatField()
    rating_stddev = models.FloatField()
    ladder_points = models.IntegerField()
    ladder_search_radius = models.IntegerField()
    total_queue_time = models.FloatField()
    pending_mm_id = models.IntegerField(null=True)
    wins = models.IntegerField()
    losses = models.IntegerField()
