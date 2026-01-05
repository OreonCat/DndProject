from django.urls import path

from game import views
from game.views import DamageFormView, HealthFormView, SetInitiativeFormView, StartEncounterRedirect, \
    NextStepEncounterRedirect

app_name = 'game'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game-list'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('game/create', views.CreateGameView.as_view(), name='game-create'),
    path('encounter/<int:pk>', views.EncounterDetailView.as_view(), name='encounter-detail'),
    path('encounter/create/<int:pk>', views.CreateEncounterRedirect.as_view(), name='encounter-redirect'),
    path('game/<int:pk>/add_character', views.CharacterAddToGameListView.as_view(), name='game-add-character'),
    path('game/add_character_redirects/<int:game_id>/<int:character_id>', views.AddCharacterToGameRedirect.as_view(), name='game-add-character-redirects'),
    path('encounter/<int:pk>/add_hero', views.HeroAddToEncounterListView.as_view(), name='encounter-add-hero'),
    path('encounter/add_hero_redirects/<int:game_id>/<int:character_id>', views.HeroAddToEncounterRedirect.as_view(), name='encounter-add-hero-redirects'),
    path('encounter/<int:pk>/add_enemy', views.EnemyAddToEncounterListView.as_view(), name="encounter-add-enemy"),
    path('encounter/add_enemy_redirects/<int:game_id>/<int:character_id>', views.EnemyAddToEncounterRedirect.as_view(), name="encounter-add-enemy-redirects"),
    path('encounter/delete_character/<int:encounter_id>/<int:pk>', views.DeleteCharacterFromEncounterRedirect.as_view(), name="encounter-delete-character"),
    path('encounter/character_get_damage/<int:pk>', DamageFormView.as_view(), name='encounter-character-get-damage'),
    path('encounter/character_get_health/<int:pk>', HealthFormView.as_view(), name='encounter-character-get-health'),
    path('encounter/character_get_initiative/<int:pk>', SetInitiativeFormView.as_view(), name='encounter-character-get-initiative'),
    path('encounter/start/<int:pk>', StartEncounterRedirect.as_view(), name='encounter-start'),
    path('encounter/next_step/<int:pk>', NextStepEncounterRedirect.as_view(), name='encounter-next-step'),
]
