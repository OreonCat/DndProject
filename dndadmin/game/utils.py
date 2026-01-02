from characterapp.utils import BaseMixin, SearchMixin


class MasterInfoMixin(SearchMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master_username'] = self.request.user.username
        context['master_realname'] = f"{self.request.user.first_name} {self.request.user.last_name}"
        return context