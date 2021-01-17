from django.urls import path

from webapp import views

urlpatterns = [
    path('hello_world', views.hello_world, name='hello_world'),
]
