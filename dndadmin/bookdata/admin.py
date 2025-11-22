from django.contrib import admin

from bookdata.models import DndClass, Race, Background


# Register your models here.
@admin.register(DndClass)
class DndClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)