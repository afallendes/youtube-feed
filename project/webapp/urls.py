from django.urls import path

from webapp import views

urlpatterns = [
    path('add_channel', views.add_channel, name='add_channel'),
    path('', views.list_videos, name='list_videos')
]
