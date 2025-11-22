from django.urls import path
from characterapp import views

app_name = 'characters'

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='character-list'),
    path('add/', views.CharacterCreateView.as_view(), name='character-add'),
]
