from django.urls import path

from game import views

app_name = 'game'

urlpatterns = [
    path('', views.PlaceHolderTemplateView.as_view(), name='game-list'),
]
