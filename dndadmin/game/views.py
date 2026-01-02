from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, RedirectView

from characterapp.models import Character
from characterapp.utils import BaseMixin, CharacterListMixin
from game.forms import GameForm, GameSearchForm
from game.models import Game, Encounter
from game.utils import MasterInfoMixin
from django.db.models import Value, BooleanField


class GameListView(LoginRequiredMixin, MasterInfoMixin, ListView):
    model = Game
    paginate_by = 10
    context_object_name = 'games'
    template_name = 'game/game_list.html'
    title_page = "Игры"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GameSearchForm()
        return context

    def get_queryset(self):
        game_objects = Game.objects.filter(master=self.request.user)
        if self.request.GET.get('name'):
            game_objects = game_objects.filter(name__icontains=self.request.GET.get('name'))
        return game_objects

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['game'].name
        context['characters'] = context['game'].characters.all()
        return context

class CreateGameView(LoginRequiredMixin, BaseMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game/game_form.html'
    title_page = "Новая игра"

    def form_valid(self, form):
        game = form.save(commit=False)
        game.master = self.request.user
        game.save()
        return super().form_valid(form)

class EncounterDetailView(LoginRequiredMixin, BaseMixin, DetailView):
    model = Encounter
    context_object_name = 'encounter'
    template_name = 'game/encounter_detail.html'
    title_page = "Бой"

class CreateEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        encounter = Encounter.objects.create(game_id=self.kwargs['pk'])
        encounter.save()
        return encounter.get_absolute_url()

class CharacterAddToGameListView(LoginRequiredMixin, CharacterListMixin, ListView):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'game/add_character_to_game.html'
    title_page = "Игровые персонажи"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_player=True).exclude(games__in=[self.kwargs['pk']])

class AddCharacterToGameRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs['game_id'])
        character = Character.objects.get(pk=self.kwargs['character_id'])
        game.characters.add(character)
        game.save()
        return game.get_absolute_url()



