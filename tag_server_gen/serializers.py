from rest_framework import serializers
from .models import *


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ('id', 'name', 'pseudoname', 'email', 'password', 'phone_number','date_creation','birthday','user_log_ip')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','type_game','duration','game_status','private','longitude','latitude','game_name')


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ('id','player','in_game','game','admin','creation_time','kicked','time_kicked','team')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','sender_id','receiver_id','game','tag_time')


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ('id','sender','receiver','time_sent','opened','time_opened','game')


class LocatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocatePlayer
        fields = ('id','game','player','longitude','latitude')