from django.urls import path, include, re_path

from api import views

app_name = 'api'

urlpatterns = [
    path('bookdata/dndclass', views.DndClassApiView.as_view(), name='dndclass'),
    path('bookdata/race', views.DndRaceApiView.as_view(), name='dndrace'),
    path('my_username', views.GetUsernameApiView.as_view(), name='username'),
    path('characters', views.CharacterApiView.as_view(), name='characters'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]