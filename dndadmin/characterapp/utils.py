from characterapp.forms import SearchForm
from characterapp.models import Character


class BaseMixin:
    title_page = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title_page:
            context['title'] = self.title_page
        return context


class CharacterListMixin(BaseMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['url_clean'] = f"{self.request.scheme}://{self.request.get_host()}{self.request.path}"
        return context

    def get_queryset(self):
        character_objects = Character.objects.all()
        if self.request.GET.get('name'):
            character_objects = character_objects.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('dnd_class'):
            character_objects = character_objects.filter(dnd_class=self.request.GET.get('dnd_class'))
        if self.request.GET.get('race'):
            character_objects = character_objects.filter(race=self.request.GET.get('race'))
        if self.request.GET.get('level'):
            character_objects = character_objects.filter(level=self.request.GET.get('level'))
        return character_objects