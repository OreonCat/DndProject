from django.urls import path
from characterapp import views

app_name = 'characters'

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='character-list'),
    path('playable/', views.PlayableCharacterListView.as_view(), name='playable-character-list'),
    path('npc/', views.NPCListView.as_view(), name='npc-list'),
    path('add/', views.CharacterCreateView.as_view(), name='character-add'),
    path('<int:pk>/', views.CharacterDetailView.as_view(), name='character-detail'),
    path('/increase_ability/<int:pk>', views.IncreaseAbility.as_view(), name='character-increase-ability'),
    path('/decrease_ability/<int:pk>', views.DecreaseAbility.as_view(), name='character-decrease-ability'),
    path('/make_proficient_ability/<int:pk>', views.MakeProficientAbility.as_view(), name='make-proficient-ability'),
    path('/make_proficient_skill/<int:pk>', views.MakeProficientSkill.as_view(), name='make-proficient-skill'),
    path('update/<int:pk>', views.CharacterUpdateView.as_view(), name='character-update'),
    path('coin_update/<int:pk>', views.CoinsUpdateView.as_view(), name='coin-update'),
    path('go_to_gold/<int:pk>', views.GoToGoldView.as_view(), name='go-to-gold'),
]
