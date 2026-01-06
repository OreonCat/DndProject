from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View

from characterapp.forms import CharacterCreateForm, CoinForm
from characterapp.models import Character, Ability, Skill
from characterapp.utils import BaseMixin, CharacterListMixin


# Create your views here.
class CharacterListView(LoginRequiredMixin, CharacterListMixin, ListView):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'characterapp/character_list.html'
    title_page = "Все персонажи"

class PlayableCharacterListView(LoginRequiredMixin, CharacterListMixin, ListView):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'characterapp/character_list.html'
    title_page = "Игровые персонажи"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_player=True)

class NPCListView(LoginRequiredMixin, CharacterListMixin, ListView):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'characterapp/character_list.html'
    title_page = "NPC"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_player=False)


class CharacterCreateView(LoginRequiredMixin, BaseMixin, CreateView):
    model = Character
    form_class = CharacterCreateForm
    template_name = 'characterapp/character_form.html'
    success_url = reverse_lazy('characters:character-list')
    title_page = "Добавить персонажа"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hp = form.instance.max_hp
        form.save()
        for ability_choice in Ability.AbilityType.choices:
            ability = Ability.objects.create(character=form.instance, ability=ability_choice[0])
            ability.save()
            Skill.create_skills(ability)

        return super().form_valid(form)

class CharacterDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'characterapp/character_detail.html'

    def test_func(self):
        return (self.request.user == self.get_object().user) or (not self.get_object().is_player)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class IncreaseAbility(View):
    def post(self, request, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        if not ability.check_master(request.user):
            raise PermissionDenied
        ability.increase()
        return redirect(ability.character.get_absolute_url())

class DecreaseAbility(View):
    def post(self, request, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        if not ability.check_master(request.user):
            raise PermissionDenied
        ability.decrease()
        return redirect(ability.character.get_absolute_url())

class MakeProficientAbility(View):
    def post(self, request, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        if not ability.check_master(request.user):
            raise PermissionDenied
        ability.make_proficient()
        return redirect(ability.character.get_absolute_url())

class MakeProficientSkill(View):
    def post(self, request, *args, **kwargs):
        skill = Skill.objects.get(pk=self.kwargs['pk'])
        if not skill.ability.check_master(request.user):
            raise PermissionDenied
        skill.make_proficient()
        return redirect(skill.ability.character.get_absolute_url())

class CharacterUpdateView(LoginRequiredMixin, UserPassesTestMixin, BaseMixin, UpdateView):
    model = Character
    form_class = CharacterCreateForm
    template_name = 'characterapp/character_form.html'
    title_page = "Редактировать персонажа"

    def test_func(self):
        return (self.request.user == self.get_object().user) or (not self.get_object().is_player)

    def get_success_url(self, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        return character.get_absolute_url()

class CoinsUpdateView(LoginRequiredMixin, UserPassesTestMixin, BaseMixin, UpdateView):
    model = Character
    form_class = CoinForm
    template_name = 'characterapp/character_form.html'
    title_page = "Управление казной"

    def test_func(self):
        return (self.request.user == self.get_object().user) or (not self.get_object().is_player)

    def get_success_url(self, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        return character.get_absolute_url()

class GoToGoldView(View):
    def post(self, request, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        character.go_to_gold()
        character.save()
        return redirect(character.get_absolute_url())