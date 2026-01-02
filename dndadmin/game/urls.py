from django.urls import path

from game import views

app_name = 'game'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('game/create', views.CreateGameView.as_view(), name='game-create'),
    path('encounter/<int:pk>', views.EncounterDetailView.as_view(), name='encounter-detail'),
    path('encounter/create/<int:pk>', views.CreateEncounterRedirect.as_view(), name='encounter-redirect'),
    path('game/<int:pk>/add_character', views.CharacterAddToGameListView.as_view(), name='game-add-character'),
    path('game/add_character_redirects/<int:game_id>/<int:character_id>', views.AddCharacterToGameRedirect.as_view(), name='game-add-character-redirects'),
]
