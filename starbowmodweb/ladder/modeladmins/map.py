from django.contrib import admin

MAP_UPDATE_SUCCESS_PREFIX = "1 map was"
MAP_UPDATE_SUCCESS_PREFIX_PLUR = "{} maps were"


class MapModelAdmin(admin.ModelAdmin):

    actions = [
        'add_to_ladder_pool',
        'remove_from_ladder_pool',
    ]

    list_display = [
        str,
        'in_ranked_pool',
    ]

    list_editable = [
        'in_ranked_pool',
    ]

    list_filter = (
        'in_ranked_pool',
        'region',
    )

    ordering = ('bnet_name',)

    search_fields = ('bnet_name',)

    def add_to_ladder_pool(self, request, queryset):
        rows_updated = queryset.update(in_ranked_pool=True)
        if rows_updated == 1:
            message_bit = MAP_UPDATE_SUCCESS_PREFIX
        else:
            message_bit = MAP_UPDATE_SUCCESS_PREFIX_PLUR.format(rows_updated)
        self.message_user(request, "%s successfully set as ladder maps." % message_bit)
    add_to_ladder_pool.short_description = "Set selected maps as ladder maps"

    def remove_from_ladder_pool(self, request, queryset):
        rows_updated = queryset.update(in_ranked_pool=False)
        if rows_updated == 1:
            message_bit = MAP_UPDATE_SUCCESS_PREFIX
        else:
            message_bit = MAP_UPDATE_SUCCESS_PREFIX_PLUR.format(rows_updated)
        self.message_user(request, "%s successfully set as unranked maps." % message_bit)
    remove_from_ladder_pool.short_description = "Set selected maps as unranked maps"
