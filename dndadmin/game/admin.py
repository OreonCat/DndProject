from django.contrib import admin

from game.models import Game, Encounter


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'time_start')