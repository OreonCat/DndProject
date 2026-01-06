from django.urls import path

from game import views

app_name = 'game'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('game/create', views.CreateGameView.as_view(), name='game-create'),
    path('encounter/<int:pk>', views.EncounterDetailView.as_view(), name='encounter-detail'),
    path('encounter/create/<int:pk>', views.CreateEncounter.as_view(), name='encounter-redirect'),
    path('game/<int:pk>/add_character', views.CharacterAddToGameListView.as_view(), name='game-add-character'),
    path('game/add_character_redirects/<int:game_id>/<int:character_id>', views.AddCharacterToGame.as_view(), name='game-add-character-redirects'),
    path('encounter/<int:pk>/add_hero', views.HeroAddToEncounterListView.as_view(), name='encounter-add-hero'),
    path('encounter/add_hero_redirects/<int:game_id>/<int:character_id>', views.HeroAddToEncounter.as_view(), name='encounter-add-hero-redirects'),
    path('encounter/<int:pk>/add_enemy', views.EnemyAddToEncounterListView.as_view(), name="encounter-add-enemy"),
    path('encounter/add_enemy_redirects/<int:game_id>/<int:character_id>', views.EnemyAddToEncounter.as_view(), name="encounter-add-enemy-redirects"),
    path('encounter/delete_character/<int:encounter_id>/<int:pk>', views.DeleteCharacterFromEncounter.as_view(), name="encounter-delete-character"),
    path('encounter/character_get_damage/<int:pk>', views.DamageFormView.as_view(), name='encounter-character-get-damage'),
    path('encounter/character_get_health/<int:pk>', views.HealthFormView.as_view(), name='encounter-character-get-health'),
    path('encounter/character_get_initiative/<int:pk>', views.SetInitiativeFormView.as_view(), name='encounter-character-get-initiative'),
    path('encounter/start/<int:pk>', views.StartEncounterView.as_view(), name='encounter-start'),
    path('encounter/next_step/<int:pk>', views.NextStepEncounter.as_view(), name='encounter-next-step'),
    path('encounter/close/<int:pk>', views.CloseEncounterView.as_view(), name='encounter-close'),
]
