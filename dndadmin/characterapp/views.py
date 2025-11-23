from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, RedirectView, UpdateView

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

class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'characterapp/character_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

class IncreaseAbility(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        ability.value = ability.value + 1
        ability.saving_throw = ability.saving_throw + 1
        ability.save()
        for skill in ability.skills.all():
            skill.value = skill.value + 1
            skill.save()
        return ability.character.get_absolute_url()

class DecreaseAbility(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        ability.value = ability.value - 1
        ability.saving_throw = ability.saving_throw - 1
        ability.save()
        for skill in ability.skills.all():
            skill.value = skill.value - 1
            skill.save()
        return ability.character.get_absolute_url()

class MakeProficientAbility(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        ability = Ability.objects.get(pk=self.kwargs['pk'])
        if ability.is_proficient:
            ability.is_proficient = False
            ability.saving_throw = ability.saving_throw - ability.character.proficient_bonus
            ability.save()
        else:
            ability.is_proficient = True
            ability.saving_throw = ability.saving_throw + ability.character.proficient_bonus
            ability.save()
        return ability.character.get_absolute_url()

class MakeProficientSkill(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        skill = Skill.objects.get(pk=self.kwargs['pk'])
        character = skill.ability.character
        if skill.is_proficient:
            skill.is_proficient = False
            skill.value = skill.value - character.proficient_bonus
            skill.save()
        else:
            skill.is_proficient = True
            skill.value = skill.value + character.proficient_bonus
            skill.save()
        return character.get_absolute_url()

class CharacterUpdateView(LoginRequiredMixin, BaseMixin, UpdateView):
    model = Character
    form_class = CharacterCreateForm
    template_name = 'characterapp/character_form.html'
    title_page = "Редактировать персонажа"

    def get_success_url(self, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        return character.get_absolute_url()

class CoinsUpdateView(LoginRequiredMixin, BaseMixin, UpdateView):
    model = Character
    form_class = CoinForm
    template_name = 'characterapp/character_form.html'
    title_page = "Управление казной"

    def get_success_url(self, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        return character.get_absolute_url()

class GoToGoldView(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        character = Character.objects.get(pk=self.kwargs['pk'])
        character.go_to_gold()
        character.save()
        return character.get_absolute_url()


