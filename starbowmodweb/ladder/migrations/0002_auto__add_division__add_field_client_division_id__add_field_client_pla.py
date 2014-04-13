# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Division'
        db.create_table('divisions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('promotion_threshold', self.gf('django.db.models.fields.FloatField')()),
            ('demotion_threshold', self.gf('django.db.models.fields.FloatField')()),
            ('icon_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('small_icon_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ladder_group', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ladder', ['Division'])

        # Adding field 'Client.division'
        db.add_column('clients', 'division',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.Division'], null=True, db_column='division_id'),
                      keep_default=False)

        # Adding field 'Client.placement_matches_remaining'
        db.add_column('clients', 'placement_matches_remaining',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ClientRegionStats.division'
        db.add_column('client_region_stats', 'division',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ladder.Division'], null=True, db_column='division_id'),
                      keep_default=False)

        # Adding field 'ClientRegionStats.placement_matches_remaining'
        db.add_column('client_region_stats', 'placement_matches_remaining',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Map.description'
        db.add_column('maps', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_column='Description'),
                      keep_default=False)

        # Adding field 'Map.info_url'
        db.add_column('maps', 'info_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_column='InfoUrl'),
                      keep_default=False)

        # Adding field 'Map.preview_url'
        db.add_column('maps', 'preview_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_column='PreviewUrl'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Division'
        db.delete_table('divisions')

        # Deleting field 'Client.division'
        db.delete_column('clients', 'division_id')

        # Deleting field 'Client.placement_matches_remaining'
        db.delete_column('clients', 'placement_matches_remaining')

        # Deleting field 'ClientRegionStats.division'
        db.delete_column('client_region_stats', 'division_id')

        # Deleting field 'ClientRegionStats.placement_matches_remaining'
        db.delete_column('client_region_stats', 'placement_matches_remaining')

        # Deleting field 'Map.description'
        db.delete_column('maps', 'Description')

        # Deleting field 'Map.info_url'
        db.delete_column('maps', 'InfoUrl')

        # Deleting field 'Map.preview_url'
        db.delete_column('maps', 'PreviewUrl')


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
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.Division']", 'null': 'True', 'db_column': "'division_id'"}),
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
            'placement_matches_remaining': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_mean': ('django.db.models.fields.FloatField', [], {}),
            'rating_stddev': ('django.db.models.fields.FloatField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'ladder.clientregionstats': {
            'Meta': {'object_name': 'ClientRegionStats', 'db_table': "'client_region_stats'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': u"orm['ladder.Client']"}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ladder.Division']", 'null': 'True', 'db_column': "'division_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ladder_forefeits': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_losses': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_points': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_walkovers': ('django.db.models.fields.IntegerField', [], {}),
            'ladder_wins': ('django.db.models.fields.IntegerField', [], {}),
            'placement_matches_remaining': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
        u'ladder.division': {
            'Meta': {'object_name': 'Division', 'db_table': "'divisions'"},
            'demotion_threshold': ('django.db.models.fields.FloatField', [], {}),
            'icon_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ladder_group': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'promotion_threshold': ('django.db.models.fields.FloatField', [], {}),
            'small_icon_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ladder.map': {
            'Meta': {'unique_together': "(('region', 'bnet_name'),)", 'object_name': 'Map', 'db_table': "'maps'"},
            'bnet_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'BattleNetID'"}),
            'bnet_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'BattleNetName'"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_column': "'Description'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_ranked_pool': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'InRankedPool'"}),
            'info_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_column': "'InfoUrl'"}),
            'preview_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_column': "'PreviewUrl'"}),
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
            'authtoken': ('django.db.models.fields.CharField', [], {'default': "'c4db7e88b2ba834f0ebef229a1bc21'", 'unique': 'True', 'max_length': '48'}),
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