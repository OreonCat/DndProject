from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('bookdata/dndclass', views.DndClassApiView.as_view(), name='dndclass'),
]