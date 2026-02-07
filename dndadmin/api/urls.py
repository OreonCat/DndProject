from django.urls import path, include, re_path

from api import views

app_name = 'api'

urlpatterns = [
    path('bookdata/dndclass', views.DndClassApiView.as_view(), name='dndclass'),
    path('bookdata/race', views.DndRaceApiView.as_view(), name='dndrace'),
    path('bookdata/background', views.DndBackgroundApiView.as_view(), name='dndbackground'),
    path('my_username', views.GetUsernameApiView.as_view(), name='username'),
    path('characters', views.CharacterApiView.as_view(), name='characters'),
    path('characters/update/<int:pk>', views.CharacterInsertApiView.as_view(), name='characterupdate'),
    path('characters/create', views.CharacterCreateApiView.as_view(), name='charactercreate'),
    path('abilities/update/<int:pk>', views.AbilityUpdateApiView.as_view(), name='abilityupdate'),
    path('skills/update/<int:pk>', views.SkillUpdateApiView.as_view(), name='skillupdate'),
    path('games', views.GameListApiView.as_view(), name='games'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]