from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='game-home'),
    path('lobby/new/', views.LobbyCreateView.as_view(), name='create-lobby'),
    path('lobby/<int:pk>/delete', views.LobbyDeleteView.as_view(), name='lobby-delete'),
    path('lobby/<int:pk>/player', views.custom_player_detail, name='lobby-player'),
    path('lobby/connect', views.lobby_connect, name='lobby-connect'),
    path('lobby/<int:pk>', views.custom_lobby_detail_view, name='lobby')
]