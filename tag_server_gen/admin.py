from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Players)
admin.site.register(Game)
admin.site.register(Lobby)
admin.site.register(Tag)
admin.site.register(Invite)
admin.site.register(LocatePlayer)
