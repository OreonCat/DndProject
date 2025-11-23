from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('change_password/', views.UserPasswordChangeView.as_view(), name='change_password'),
]