from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, RedirectView, FormView

from characterapp.models import Character
from characterapp.utils import BaseMixin, CharacterListMixin
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

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'game/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['game'].name
        context['characters'] = context['game'].characters.all()
        context['encounters'] = context['game'].encounters.all()
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

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['characters'] = context['encounter'].encounter_characters.all().order_by('-initiative')
        return context



class CreateEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        game = Game.objects.get(pk=self.kwargs['pk'])
        encounter = Encounter.objects.create(game = game)
        encounter.save()
        characters = game.characters.all()
        for character in characters:
            enc_char = EncounterCharacter.objects.create(character = character, encounter = encounter)
            enc_char.save()
        return encounter.get_absolute_url()

class CharacterAddToGameListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:game-add-character-redirects'

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

class HeroAddToEncounterListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:encounter-add-hero-redirects'

class HeroAddToEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['game_id'])
        encounter_character = EncounterCharacter.objects.create(encounter_id = self.kwargs['game_id'], character_id = self.kwargs['character_id'])
        encounter_character.save()
        return encounter.get_absolute_url()

class EnemyAddToEncounterListView(LoginRequiredMixin, AddCharacterMixin, ListView):
    add_url = 'game:encounter-add-enemy-redirects'

class EnemyAddToEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        encounter = Encounter.objects.get(pk=self.kwargs['game_id'])
        encounter_character = EncounterCharacter.objects.create(encounter_id = self.kwargs['game_id'], character_id = self.kwargs['character_id'], is_enemy=True)
        encounter_character.save()
        return encounter.get_absolute_url()

class DeleteCharacterFromEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        character = EncounterCharacter.objects.get(pk=self.kwargs['pk'])
        character.delete()
        encounter = Encounter.objects.get(pk=self.kwargs['encounter_id'])
        return encounter.get_absolute_url()

class DamageFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Нанести урон"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk']).character
        character.get_damage(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class HealthFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Лечение"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk']).character
        character.get_health(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class SetInitiativeFormView(LoginRequiredMixin, BaseMixin, FormView):
    template_name = 'game/game_form.html'
    form_class = HitPointForm
    title_page = "Внести инициативу"

    def form_valid(self, form):
        character = EncounterCharacter.objects.get(pk = self.kwargs['pk'])
        character.set_initiative(form.cleaned_data['value'])
        return super().form_valid(form)

    def get_success_url(self):
        return EncounterCharacter.objects.get(pk = self.kwargs['pk']).encounter.get_absolute_url()

class StartEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        encounter = Encounter.objects.get(pk = self.kwargs['pk'])
        if encounter.is_start:
            return encounter.get_absolute_url()
        else:
            encounter.start()
            return encounter.get_absolute_url()

class NextStepEncounterRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        encounter = Encounter.objects.get(pk = self.kwargs['pk'])
        encounter.next_step()
        return encounter.get_absolute_url()




