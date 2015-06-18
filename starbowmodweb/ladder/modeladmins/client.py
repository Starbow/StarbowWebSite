from django.contrib import admin


class ClientModelAdmin(admin.ModelAdmin):
    search_fields = ('username',)
