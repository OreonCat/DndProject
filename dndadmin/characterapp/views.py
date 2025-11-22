from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from characterapp.forms import CharacterCreateForm
from characterapp.models import Character, Ability, Skill


# Create your views here.
class CharacterListView(ListView):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'characterapp/character_list.html'

class CharacterCreateView(CreateView):
    model = Character
    form_class = CharacterCreateForm
    template_name = 'characterapp/character_form.html'
    success_url = reverse_lazy('characters:character-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hp = form.instance.max_hp
        form.save()
        for ability_choice in Ability.AbilityType.choices:
            ability = Ability.objects.create(character=form.instance, ability=ability_choice[0])
            ability.save()
            Skill.create_skills(ability)

        return super().form_valid(form)
