from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse

from characterapp.models import Character
from characterapp.utils import BaseMixin, SearchMixin, CharacterListMixin
from game.models import Encounter


class MasterInfoMixin(SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master_username'] = self.request.user.username
        context['master_realname'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        return context

class AddCharacterMixin(CharacterListMixin):
    model = Character
    context_object_name = 'characters'
    paginate_by = 10
    template_name = 'game/add_character_to_game.html'
    title_page = "Игровые персонажи"
    add_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_pk'] = self.kwargs['pk']
        if self.add_url:
            context['add_url'] = self.add_url
        return context


