from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [


    # Get functions URLs
    path('player_info', views.player_data),
    path('lobby_info', views.lobby_info),
    path('game_info', views.game_info),
    path('tags', views.get_game_tags_player),
    path('invites', views.get_invites),
    path('teams', views.teams),
    path('games_list', views.get_games_list),
    path('start_game', views.start_game),


    # Post functions URLs
    path('get_invites', views.get_invites),
    path('player_register', views.register_player),
    path('create_game', views.create_game),
    path('player_login', views.player_login),
    path('player_logout', views.player_logout),
    path('join_lobby', views.add_to_lobby),
    path('kick_player',views.kick_from_lobby),
    path('player_ready', views.player_ready)


]


urlpatterns = format_suffix_patterns(urlpatterns)