from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView, UpdateView

from characterapp.utils import BaseMixin


class UserLoginView(BaseMixin, LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('game:game-list')
    form_class = AuthenticationForm
    title_page = "Войти"

class UserLogoutView(RedirectView):
    permanent = False
    query_string = True
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse_lazy('game:game-list')

class UserRegisterView(BaseMixin, CreateView):
    template_name = 'users/login.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('game:game-list')
    title_page = "Регистрация"

class UserUpdateView(LoginRequiredMixin, BaseMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('users:update')
    title_page = "Изменить профиль"

    def get_object(self):
        return self.request.user

class UserPasswordChangeView(LoginRequiredMixin, BaseMixin, PasswordChangeView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:update')
    title_page = "Сменить пароль"
