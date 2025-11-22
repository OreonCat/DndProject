from django.shortcuts import render
from django.views.generic import TemplateView


class PlaceHolderTemplateView(TemplateView):
    template_name = 'game/game_list.html'
