from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class PlaceHolderTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'game/game_list.html'
