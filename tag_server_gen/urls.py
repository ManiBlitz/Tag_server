from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [


    # Get functions URLs
    path('player_info', views.player_data),             #INSERTED
    path('lobby_info', views.lobby_info),               #INSERTED
    path('lobby_row_info', views.lobby_row_info),       #INSERTED
    path('game_info', views.game_info),                 #INSERTED
    path('invite_info', views.invite_info),             #INSERTED
    path('tags', views.get_game_tags_player),           #INSERTED
    path('invites', views.get_invites),                 #INSERTED
    path('games_list', views.get_games_list),           #INSERTED
    path('start_game', views.start_game),               #INSERTED
    path('locate_fetch', views.locate_fetch),           #INSERTED
    path('end_game', views.end_game),                   #INSERTED


    # Post functions URLs
    path('send_invite', views.send_invite),             #INSERTED
    path('open_invite', views.open_invite),             #INSERTED
    path('player_register', views.register_player),     #INSERTED
    path('create_game', views.create_game),             #INSERTED
    path('player_login', views.player_login),           #INSERTED
    path('player_logout', views.player_logout),         #INSERTED
    path('join_lobby', views.add_to_lobby),             #INSERTED
    path('kick_player',views.kick_from_lobby),          #INSERTED
    path('player_ready', views.player_ready),           #INSERTED
    path('locate_player', views.update_location_player),#INSERTED
    path('tagged', views.player_tagged),                #INSERTED
    path("quit_lobby", views.quit_lobby)                #INSERTED


]


urlpatterns = format_suffix_patterns(urlpatterns)