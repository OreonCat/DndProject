from django.contrib import admin

from characterapp.models import Character, Ability, Skill


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'user')
    search_fields = ('name',)

@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('ability', 'character')
    search_fields = ('ability',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'ability')
    search_fields = ('skill',)