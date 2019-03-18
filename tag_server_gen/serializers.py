from rest_framework import serializers
from .models import *


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ('id', 'name', 'pseudoname', 'email', 'password', 'phone_number','date_creation','birthday','user_log_ip')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','type_game','duration','game_status')


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ('id','player','in_game','admin','admin','creation_time')


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('id','game','team_id')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','sender_id','receiver_id','game')


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ('id','sender','receiver','time_sent','opened','lobby')