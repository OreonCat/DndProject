from django.contrib import admin

from characterapp.models import Character, Ability, Skill


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'user', 'slug')
    search_fields = ('name',)

@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('ability', 'character', 'value')
    search_fields = ('ability',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'ability', 'value')
    search_fields = ('skill',)