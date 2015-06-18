from django.contrib import admin
from starbowmodweb.ladder.models import Map, Client, BattleNetCharacter, CrashReport

import modeladmins

admin.site.register(Map, modeladmins.MapModelAdmin)
admin.site.register(Client, modeladmins.ClientModelAdmin)
# admin.site.register(ClientRegionStats)
# admin.site.register(MatchmakerMatch)
# admin.site.register(MatchmakerMatchParticipant)
# admin.site.register(MatchResultPlayer)
# admin.site.register(MatchResult)
admin.site.register(BattleNetCharacter)
admin.site.register(CrashReport)
