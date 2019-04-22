from django.db import models
from django.core.validators import RegexValidator


class Players(models.Model):
    name = models.CharField(max_length=200)
    pseudoname = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.BinaryField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    date_creation = models.DateField(auto_now_add=True)
    birthday = models.DateField(blank=False, default="1999-01-01")
    user_log_ip = models.CharField(max_length=300, blank=True)


class Game(models.Model):
    type_game = models.IntegerField(default=1)
    game_name = models.CharField(max_length=200)
    duration = models.IntegerField(default=300)
    game_status = models.IntegerField(default=1001)
    private = models.BooleanField(default=False)
    longitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=10)
    latitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=10)


class Lobby(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    in_game = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    kicked = models.BooleanField(default=False)
    time_kicked = models.DateTimeField(null=True)
    team = models.IntegerField(default=0)


class Tag(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tag_time = models.DateField(auto_now_add=True)


class Invite(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sender = models.IntegerField()
    receiver = models.IntegerField()
    time_sent = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    time_opened = models.DateTimeField(null=True)


# This particular class enables to manage in-game localization for the different players

class LocatePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.IntegerField()
    longitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=10)
    latitude = models.DecimalField(default=0.0, decimal_places=5, max_digits=10)






