from django.db import models
from datetime import datetime
from starbowmodweb.user.models import User
from django.core.urlresolvers import reverse
from django.conf import settings


BATTLENET_REGION_UNKNOWN = 0
BATTLENET_REGION_NA = 1
BATTLENET_REGION_EU = 2
BATTLENET_REGION_KR = 3
BATTLENET_REGION_CN = 5
BATTLENET_REGION_SEA = 6


REGION_CHOICES = dict([
    (BATTLENET_REGION_NA, 'NA'),
    (BATTLENET_REGION_EU, 'EU'),
    (BATTLENET_REGION_KR, 'KR'),
    (BATTLENET_REGION_CN, 'CN'),
    (BATTLENET_REGION_SEA, 'SEA'),
])
REGION_LOOKUP = dict(zip(dict(REGION_CHOICES).values(), dict(REGION_CHOICES).keys()))


class Map(models.Model):
    class Meta(object):
        db_table = 'maps'
        verbose_name = "Map"
        verbose_name_plural = "Maps"
        unique_together = ('region', 'bnet_name')

    region = models.IntegerField(
        db_column='Region',
        choices=REGION_CHOICES.items(),
        help_text="The region that this map is uploaded to. Each region needs a separate map entry",
    )

    bnet_id = models.IntegerField(
        db_column='BattleNetID',
        help_text="The XXXX in starcraft://map/XXXX; Used to construct a link to the map.",
    )

    bnet_name = models.CharField(
        max_length=255,
        db_column='BattleNetName',
        help_text="The exact name of the map.",
    )

    in_ranked_pool = models.BooleanField(
        db_column='InRankedPool',
        help_text="True for maps that are currently part of the map pool on this region.",
        default=True,
    )

    def clean(self):
        if self.bnet_name is not None:
            self.bnet_name = self.bnet_name.strip()

    def get_absolute_url(self):
        return reverse('starbowmodweb.ladder.views.show_map', args=[self.pk])

    def __str__(self):
        ranked_str = "Ranked" if self.in_ranked_pool else "Unranked"
        return "{} - {} [{}]".format(self.get_region_display(), self.bnet_name, ranked_str)


class Client(models.Model):
    class Meta(object):
        db_table = 'clients'
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    id = models.ForeignKey(User, db_column='Id', primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    rating_mean = models.FloatField()
    rating_stddev = models.FloatField()
    ladder_points = models.IntegerField()
    ladder_search_region = models.IntegerField()
    ladder_search_radius = models.IntegerField()
    matchmaking_pending_match_id = models.IntegerField(null=True)
    matchmaking_pending_opponent_id = models.IntegerField(null=True)
    matchmaking_pending_region = models.IntegerField(null=True)
    ladder_wins = models.IntegerField()
    ladder_losses = models.IntegerField()
    ladder_forefeits = models.IntegerField()
    ladder_walkovers = models.IntegerField()

    def get_absolute_url(self):
        return reverse('starbowmodweb.ladder.views.show_player', args=[self.pk])

    def __str__(self):
        return self.username


class BattleNetCharacter(models.Model):
    class Meta(object):
        db_table = 'battle_net_characters'
        verbose_name = "BNet Character"
        verbose_name_plural = "BNet Characters"

    id = models.AutoField(primary_key=True, db_column='Id')
    client = models.ForeignKey('Client', db_column='ClientId', related_name='characters', null=True)
    add_time = models.IntegerField(db_column='AddTime')
    region = models.IntegerField(db_column='Region', choices=REGION_CHOICES.items())
    subregion = models.IntegerField(db_column='SubRegion')
    toon_id = models.IntegerField(db_column='ProfileId')
    code = models.IntegerField(db_column='CharacterCode')
    toon_handle = models.CharField(max_length=255, db_column='CharacterName')
    ingame_link = models.CharField(max_length=255, db_column='InGameProfileLink')
    is_verified = models.BooleanField(db_column='IsVerified')
    verification_portrait = models.IntegerField(db_column='VerificationRequestedPortrait')

    def get_absolute_url(self):
        url = "http://{}.battle.net/sc2/profile/{}/{}/{}/"
        return url.format(self.get_region_display().lower(), self.toon_id, self.subregion, self.toon_handle)

    def __str__(self):
        return "[{}] {}".format(self.get_region_display(), self.toon_handle)


class ClientRegionStats(models.Model):
    class Meta(object):
        db_table = 'client_region_stats'
        verbose_name = "Client Region Stats"
        verbose_name_plural = "Client Region Stats"

    client = models.ForeignKey('Client', related_name='stats')
    region = models.IntegerField(choices=REGION_CHOICES.items())
    rating_mean = models.FloatField()
    rating_stddev = models.FloatField()
    ladder_points = models.IntegerField()
    ladder_wins = models.IntegerField()
    ladder_losses = models.IntegerField()
    ladder_forefeits = models.IntegerField()
    ladder_walkovers = models.IntegerField()

    # def get_absolute_url(self):
    #     return reverse('starbowmodweb.ladder.views.show_region_stats', args=[self.client.pk, self.region])

    def __str__(self):
        return "{}: {} - {}".format(self.get_region_display(), self.ladder_wins, self.ladder_losses)


class MatchmakerMatch(models.Model):
    class Meta(object):
        db_table = 'matchmaker_matches'

    id = models.AutoField(primary_key=True, db_column='Id')
    map = models.ForeignKey('Map', db_column='MapId', null=True)
    add_time = models.IntegerField(db_column='AddTime')
    end_time = models.IntegerField(db_column='EndTime')
    quality = models.FloatField(db_column='Quality')
    region = models.IntegerField(db_column='Region', choices=REGION_CHOICES.items())
    channel = models.CharField(max_length=255, db_column='Channel')
    chat_room = models.CharField(max_length=255, db_column='ChatRoom')


class MatchResultPlayer(models.Model):
    RACES = (
        (0, 'Protoss'),
        (1, 'Terran'),
        (2, 'Zerg'),
    )

    class Meta(object):
        db_table = 'match_result_players'

    id = models.AutoField(primary_key=True, db_column='Id')
    client = models.ForeignKey('Client', db_column='ClientId', related_name='results', null=True)
    match = models.ForeignKey('MatchResult', db_column='MatchId', related_name='players', null=True)
    character = models.ForeignKey('BattleNetCharacter', db_column='CharacterId', null=True)
    points_before = models.IntegerField(db_column='PointsBefore')
    points_after = models.IntegerField(db_column='PointsAfter')
    point_difference = models.IntegerField(db_column='PointsDifference')
    race = models.CharField(max_length=255, db_column='Race', choices=RACES)
    victory = models.IntegerField(db_column='Victory')


class MatchResult(models.Model):
    class Meta(object):
        db_table = 'match_results'

    id = models.AutoField(primary_key=True, db_column='Id')
    matchmaker_match = models.ForeignKey('MatchmakerMatch', db_column='MatchmakerMatchId', null=True)
    datetime = models.IntegerField(db_column='DateTime')
    region = models.IntegerField(db_column='Region', choices=REGION_CHOICES.items())
    map = models.ForeignKey('Map', db_column='MapId', null=True)


class MatchmakerMatchParticipant(models.Model):
    class Meta(object):
        db_table = 'matchmaker_match_participants'

    id = models.AutoField(primary_key=True, db_column='Id')
    client = models.ForeignKey('Client', db_column='ClientId', null=True)
    matchmaker_match = models.ForeignKey('MatchmakerMatch', db_column='MatchId', null=True)
    points = models.IntegerField(db_column='Points')
    rating_mean = models.FloatField(db_column='RatingMean')
    rating_stddev = models.FloatField(db_column='RatingStdDev')
    queue_time = models.FloatField(db_column='QueueTime')


def get_crash_report_name(instance, filename=""):
    report_date = instance.time or datetime.now()
    return "crashreport/{}/{}/{}.{}.dmp".format(
        instance.client_version,
        instance.os,
        instance.user.username,
        report_date.strftime('D%Y%m%d.T%H%M%S')
    )


class CrashReport(models.Model):
    user = models.ForeignKey(User, related_name="crash_reports", null=True)
    os = models.CharField(max_length=255, choices=settings.OS_CHOICES, help_text="The operating system you were running.")
    client_version = models.IntegerField(max_length=255, choices=settings.CLIENT_VERSIONS, help_text="The version of the client you were running.")
    description = models.TextField(help_text="(Optional) Please describe how the crash occured. Be specific as possible.", blank=True)
    dump = models.FileField(upload_to=get_crash_report_name, help_text="The .dmp file will be next to your eros executable.<br/>You can delete the file after submitting it here. We will always be accessible to you on your user homepage.")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Client v"+get_crash_report_name(self).split('/', 1)[1]
