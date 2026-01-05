from django.contrib import admin

from game.models import Game, Encounter, EncounterCharacter


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'time_start')

@admin.register(EncounterCharacter)
class EncounterCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'character', 'encounter', 'is_enemy', 'initiative')