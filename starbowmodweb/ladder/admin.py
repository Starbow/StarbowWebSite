from django.contrib import admin
from starbowmodweb.ladder.models import Map, Client, BattleNetCharacter, CrashReport

from modeladmins import MapModelAdmin

admin.site.register(Map, MapModelAdmin)
admin.site.register(Client)
# admin.site.register(ClientRegionStats)
# admin.site.register(MatchmakerMatch)
# admin.site.register(MatchmakerMatchParticipant)
# admin.site.register(MatchResultPlayer)
# admin.site.register(MatchResult)
admin.site.register(BattleNetCharacter)
admin.site.register(CrashReport)
