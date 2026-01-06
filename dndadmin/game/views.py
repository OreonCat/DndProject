import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, RedirectView, FormView, View

from characterapp.models import Character
from characterapp.utils import BaseMixin
from game.forms import GameForm, GameSearchForm, HitPointForm
from game.models import Game, Encounter, EncounterCharacter
from game.utils import MasterInfoMixin, AddCharacterMixin


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

class GameDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game/game_detail.html'

    def test_func(self):
        return self.request.user == self.get_object().master

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['game'].name
        context['characters'] = context['game'].characters.all()
        context['encounters'] = context['game'].encounters.all().order_by('-time_start')
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

class EncounterDetailView(LoginRequiredMixin, BaseMixin, UserPassesTestMixin, DetailView):
    model = Encounter
    context_object_name = 'encounter'
    template_name = 'game/encounter_detail.html'
    title_page = "Бой"

    def test_func(self):
        return self.request.user == self.get_object().game.master

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['characters'] = context['encounter'].encounter_characters.all().order_by('-initiative')
        return context


class CreateEncounter(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs['pk'])
        if not game.check_master(request.user):
            raise PermissionDenied
        encounter = Encounter.objects.create(game=game)
        encounter.save()
        characters = game.characters.all()
        for character in characters:
            enc_char = EncounterCharacter.objects.create(character=character, encounter=encounter, hp=character.hp,
                                                         max_hp=character.max_hp)
            enc_char.save()
        return redirect(encounter.get_absolute_url())

class CharacterAddToGameListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:game-add-character-redirects'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_player=True).exclude(games__in=[self.kwargs['pk']])

class AddCharacterToGame(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs['game_id'])
        character = Character.objects.get(pk=self.kwargs['character_id'])
        game.characters.add(character)
        game.save()
        return redirect(game.get_absolute_url())

class HeroAddToEncounterListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:encounter-add-hero-redirects'

class HeroAddToEncounter(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['game_id'])
        if not encounter.game.check_master(request.user):
            raise PermissionDenied
        character = Character.objects.get(pk=self.kwargs['character_id'])
        if encounter.is_complete:
            raise Http404
        encounter_character = EncounterCharacter.objects.create(encounter=encounter, character=character,
                                                                hp=character.hp, max_hp=character.max_hp)
        if not encounter_character.character.is_player:
            random_initiative = random.randint(1, 20)
            encounter_character.set_initiative(random_initiative)
        encounter_character.save()
        return redirect(encounter.get_absolute_url())

class EnemyAddToEncounterListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:encounter-add-enemy-redirects'

class EnemyAddToEncounter(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['game_id'])
        if not encounter.game.check_master(request.user):
            raise PermissionDenied
        character = Character.objects.get(pk=self.kwargs['character_id'])
        random_initiative = random.randint(1, 20)
        if encounter.is_complete:
            raise Http404
        encounter_character = EncounterCharacter.objects.create(encounter_id=self.kwargs['game_id'],
                                                                character_id=self.kwargs['character_id'],
                                                                hp=character.hp, max_hp=character.max_hp, is_enemy=True)
        encounter_character.set_initiative(random_initiative)
        encounter_character.save()
        return redirect(encounter.get_absolute_url())

class DeleteCharacterFromEncounter(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        character = EncounterCharacter.objects.get(pk=self.kwargs['pk'])
        if not character.encounter.game.check_master(request.user):
            raise PermissionDenied
        character.delete()
        encounter = Encounter.objects.get(pk=self.kwargs['encounter_id'])
        return redirect(encounter.get_absolute_url())

class DamageFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Нанести урон"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk'])
        if not character.encounter.game.check_master(self.request.user):
            raise PermissionDenied
        character.make_damage(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class HealthFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Лечение"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk'])
        if not character.encounter.game.check_master(self.request.user):
            raise PermissionDenied
        character.make_health(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class SetInitiativeFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Внести инициативу"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk'])
        if not character.encounter.game.check_master(self.request.user):
            raise PermissionDenied
        character.set_initiative(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class StartEncounterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['pk'])
        if not encounter.game.check_master(request.user):
            raise PermissionDenied
        if encounter.is_start:
            return encounter.get_absolute_url()
        else:
            encounter.start()
            return redirect(encounter.get_absolute_url())

class NextStepEncounter(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['pk'])
        if not encounter.game.check_master(request.user):
            raise PermissionDenied
        if encounter.is_complete:
            raise Http404
        encounter.next_step()
        return redirect(encounter.get_absolute_url())

class CloseEncounterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['pk'])
        if not encounter.game.check_master(request.user):
            raise PermissionDenied
        if encounter.is_complete:
            raise Http404
        encounter.close_encounter()
        return redirect(encounter.get_absolute_url())



