# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Map'
        db.create_table('maps', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.IntegerField')(db_column='Region')),
            ('bnet_id', self.gf('django.db.models.fields.IntegerField')(db_column='BattleNetID')),
            ('bnet_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='BattleNetName')),
            ('in_ranked_pool', self.gf('django.db.models.fields.BooleanField')(default=True, db_column='InRankedPool')),
        ))
        db.send_create_signal(u'ladder', ['Map'])

        # Adding unique constraint on 'Map', fields ['region', 'bnet_name']
        db.create_unique('maps', ['Region', 'BattleNetName'])

        # Adding model 'Client'
        db.create_table('clients', (
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user.User'], primary_key=True, db_column='Id')),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('rating_mean', self.gf('django.db.models.fields.FloatField')()),
            ('rating_stddev', self.gf('django.db.models.fields.FloatField')()),
            ('ladder_points', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_search_region', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_search_radius', self.gf('django.db.models.fields.IntegerField')()),
            ('matchmaking_pending_match_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('matchmaking_pending_opponent_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('matchmaking_pending_region', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('ladder_wins', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_losses', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_forefeits', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_walkovers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ladder', ['Client'])

        # Adding model 'BattleNetCharacter'
        db.create_table('battle_net_characters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='Id')),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='characters', null=True, db_column='ClientId', to=orm['ladder.Client'])),
            ('add_time', self.gf('django.db.models.fields.IntegerField')(db_column='AddTime')),
            ('region', self.gf('django.db.models.fields.IntegerField')(db_column='Region')),
            ('subregion', self.gf('django.db.models.fields.IntegerField')(db_column='SubRegion')),
            ('toon_id', self.gf('django.db.models.fields.IntegerField')(db_column='ProfileId')),
            ('code', self.gf('django.db.models.fields.IntegerField')(db_column='CharacterCode')),
            ('toon_handle', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='CharacterName')),
            ('ingame_link', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='InGameProfileLink')),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(db_column='IsVerified')),
            ('verification_portrait', self.gf('django.db.models.fields.IntegerField')(db_column='VerificationRequestedPortrait')),
        ))
        db.send_create_signal(u'ladder', ['BattleNetCharacter'])

        # Adding model 'ClientRegionStats'
        db.create_table('client_region_stats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['ladder.Client'])),
            ('region', self.gf('django.db.models.fields.IntegerField')()),
            ('rating_mean', self.gf('django.db.models.fields.FloatField')()),
            ('rating_stddev', self.gf('django.db.models.fields.FloatField')()),
            ('ladder_points', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_wins', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_losses', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_forefeits', self.gf('django.db.models.fields.IntegerField')()),
            ('ladder_walkovers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ladder', ['ClientRegionStats'])

        # Adding model 'MatchmakerMatch'
        db.create_table('matchmaker_matches', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='Id')),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.Map'], null=True, db_column='MapId')),
            ('add_time', self.gf('django.db.models.fields.IntegerField')(db_column='AddTime')),
            ('end_time', self.gf('django.db.models.fields.IntegerField')(db_column='EndTime')),
            ('quality', self.gf('django.db.models.fields.FloatField')(db_column='Quality')),
            ('region', self.gf('django.db.models.fields.IntegerField')(db_column='Region')),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='Channel')),
            ('chat_room', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='ChatRoom')),
        ))
        db.send_create_signal(u'ladder', ['MatchmakerMatch'])

        # Adding model 'MatchResultPlayer'
        db.create_table('match_result_players', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='Id')),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', null=True, db_column='ClientId', to=orm['ladder.Client'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', null=True, db_column='MatchId', to=orm['ladder.MatchResult'])),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.BattleNetCharacter'], null=True, db_column='CharacterId')),
            ('points_before', self.gf('django.db.models.fields.IntegerField')(db_column='PointsBefore')),
            ('points_after', self.gf('django.db.models.fields.IntegerField')(db_column='PointsAfter')),
            ('point_difference', self.gf('django.db.models.fields.IntegerField')(db_column='PointsDifference')),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='Race')),
            ('victory', self.gf('django.db.models.fields.IntegerField')(db_column='Victory')),
        ))
        db.send_create_signal(u'ladder', ['MatchResultPlayer'])

        # Adding model 'MatchResult'
        db.create_table('match_results', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='Id')),
            ('matchmaker_match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.MatchmakerMatch'], null=True, db_column='MatchmakerMatchId')),
            ('datetime', self.gf('django.db.models.fields.IntegerField')(db_column='DateTime')),
            ('region', self.gf('django.db.models.fields.IntegerField')(db_column='Region')),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.Map'], null=True, db_column='MapId')),
        ))
        db.send_create_signal(u'ladder', ['MatchResult'])

        # Adding model 'MatchmakerMatchParticipant'
        db.create_table('matchmaker_match_participants', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='Id')),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.Client'], null=True, db_column='ClientId')),
            ('matchmaker_match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.MatchmakerMatch'], null=True, db_column='MatchId')),
            ('points', self.gf('django.db.models.fields.IntegerField')(db_column='Points')),
            ('rating_mean', self.gf('django.db.models.fields.FloatField')(db_column='RatingMean')),
            ('rating_stddev', self.gf('django.db.models.fields.FloatField')(db_column='RatingStdDev')),
            ('queue_time', self.gf('django.db.models.fields.FloatField')(db_column='QueueTime')),
        ))
        db.send_create_signal(u'ladder', ['MatchmakerMatchParticipant'])

        # Adding model 'CrashReport'
        db.create_table(u'ladder_crashreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='crash_reports', null=True, to=orm['user.User'])),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('client_version', self.gf('django.db.models.fields.IntegerField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('dump', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ladder', ['CrashReport'])


    def backwards(self, orm):
        # Removing unique constraint on 'Map', fields ['region', 'bnet_name']
        db.delete_unique('maps', ['Region', 'BattleNetName'])

        # Deleting model 'Map'
        db.delete_table('maps')

        # Deleting model 'Client'
        db.delete_table('clients')

        # Deleting model 'BattleNetCharacter'
        db.delete_table('battle_net_characters')

        # Deleting model 'ClientRegionStats'
        db.delete_table('client_region_stats')

        # Deleting model 'MatchmakerMatch'
        db.delete_table('matchmaker_matches')

        # Deleting model 'MatchResultPlayer'
        db.delete_table('match_result_players')

        # Deleting model 'MatchResult'
        db.delete_table('match_results')

        # Deleting model 'MatchmakerMatchParticipant'
        db.delete_table('matchmaker_match_participants')

        # Deleting model 'CrashReport'
        db.delete_table(u'ladder_crashreport')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ladder.battlenetcharacter': {
            'Meta': {'object_name': 'BattleNetCharacter', 'db_table': "'battle_net_characters'"},
            'add_time': ('django.db.models.fields.IntegerField', [], {'db_column': "'AddTime'"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'null': 'True', 'db_column': "'ClientId'", 'to': u"orm['ladder.Client']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'db_column': "'CharacterCode'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'Id'"}),
            'ingame_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'InGameProfileLink'"}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'db_column': "'IsVerified'"}),
            'region': ('django.db.models.fields.IntegerField', [], {'db_column': "'Region'"}),
            'subregion': ('django.db.models.fields.IntegerField', [], {'db_column': "'SubRegion'"}),
            'toon_handle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'CharacterName'"}),
            'toon_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'ProfileId'"}),
            'verification_portrait': ('django.db.models.fields.IntegerField', [], {'db_column': "'VerificationRequestedPortrait'"})
        },
        u'ladder.client': {
            'Meta': {'object_name': 'Client', 'db_table': "'clients'"},
            'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user.User']", 'primary_key': 'True', 'db_column': "'Id'"}),
            'ladder_forefeits': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_losses': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_points': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_search_radius': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_search_region': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_walkovers': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_wins': ('django.db.models.fields.IntegerField', [], {}),
            'matchmaking_pending_match_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'matchmaking_pending_opponent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'matchmaking_pending_region': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rating_mean': ('django.db.models.fields.FloatField', [], {}),
            'rating_stddev': ('django.db.models.fields.FloatField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'ladder.clientregionstats': {
            'Meta': {'object_name': 'ClientRegionStats', 'db_table': "'client_region_stats'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': u"orm['ladder.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ladder_forefeits': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_losses': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_points': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_walkovers': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_wins': ('django.db.models.fields.IntegerField', [], {}),
            'rating_mean': ('django.db.models.fields.FloatField', [], {}),
            'rating_stddev': ('django.db.models.fields.FloatField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ladder.crashreport': {
            'Meta': {'object_name': 'CrashReport'},
            'client_version': ('django.db.models.fields.IntegerField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dump': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crash_reports'", 'null': 'True', 'to': u"orm['user.User']"})
        },
        u'ladder.map': {
            'Meta': {'unique_together': "(('region', 'bnet_name'),)", 'object_name': 'Map', 'db_table': "'maps'"},
            'bnet_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'BattleNetID'"}),
            'bnet_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'BattleNetName'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_ranked_pool': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'InRankedPool'"}),
            'region': ('django.db.models.fields.IntegerField', [], {'db_column': "'Region'"})
        },
        u'ladder.matchmakermatch': {
            'Meta': {'object_name': 'MatchmakerMatch', 'db_table': "'matchmaker_matches'"},
            'add_time': ('django.db.models.fields.IntegerField', [], {'db_column': "'AddTime'"}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Channel'"}),
            'chat_room': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'ChatRoom'"}),
            'end_time': ('django.db.models.fields.IntegerField', [], {'db_column': "'EndTime'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'Id'"}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.Map']", 'null': 'True', 'db_column': "'MapId'"}),
            'quality': ('django.db.models.fields.FloatField', [], {'db_column': "'Quality'"}),
            'region': ('django.db.models.fields.IntegerField', [], {'db_column': "'Region'"})
        },
        u'ladder.matchmakermatchparticipant': {
            'Meta': {'object_name': 'MatchmakerMatchParticipant', 'db_table': "'matchmaker_match_participants'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.Client']", 'null': 'True', 'db_column': "'ClientId'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'Id'"}),
            'matchmaker_match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.MatchmakerMatch']", 'null': 'True', 'db_column': "'MatchId'"}),
            'points': ('django.db.models.fields.IntegerField', [], {'db_column': "'Points'"}),
            'queue_time': ('django.db.models.fields.FloatField', [], {'db_column': "'QueueTime'"}),
            'rating_mean': ('django.db.models.fields.FloatField', [], {'db_column': "'RatingMean'"}),
            'rating_stddev': ('django.db.models.fields.FloatField', [], {'db_column': "'RatingStdDev'"})
        },
        u'ladder.matchresult': {
            'Meta': {'object_name': 'MatchResult', 'db_table': "'match_results'"},
            'datetime': ('django.db.models.fields.IntegerField', [], {'db_column': "'DateTime'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'Id'"}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.Map']", 'null': 'True', 'db_column': "'MapId'"}),
            'matchmaker_match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.MatchmakerMatch']", 'null': 'True', 'db_column': "'MatchmakerMatchId'"}),
            'region': ('django.db.models.fields.IntegerField', [], {'db_column': "'Region'"})
        },
        u'ladder.matchresultplayer': {
            'Meta': {'object_name': 'MatchResultPlayer', 'db_table': "'match_result_players'"},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.BattleNetCharacter']", 'null': 'True', 'db_column': "'CharacterId'"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'null': 'True', 'db_column': "'ClientId'", 'to': u"orm['ladder.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'Id'"}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'null': 'True', 'db_column': "'MatchId'", 'to': u"orm['ladder.MatchResult']"}),
            'point_difference': ('django.db.models.fields.IntegerField', [], {'db_column': "'PointsDifference'"}),
            'points_after': ('django.db.models.fields.IntegerField', [], {'db_column': "'PointsAfter'"}),
            'points_before': ('django.db.models.fields.IntegerField', [], {'db_column': "'PointsBefore'"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'Race'"}),
            'victory': ('django.db.models.fields.IntegerField', [], {'db_column': "'Victory'"})
        },
        u'user.user': {
            'Meta': {'object_name': 'User'},
            'authtoken': ('django.db.models.fields.CharField', [], {'default': "'d82a671377313ebaf6b29d2ff6cc29'", 'unique': 'True', 'max_length': '48'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['ladder']