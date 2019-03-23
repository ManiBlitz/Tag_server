from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from simplecrypt import encrypt, decrypt
from django.utils import timezone
import smtplib
from django.http import HttpResponse
import datetime
from datetime import datetime
import pprint

# ---
# Constants
# ---

password_encrypt = "RSMA_002_TTYHW_0101_USREF01"
date_format = "%Y-%m-%d"
valid_days_limit = 6500

# ---
# Passive references
# ---


@api_view(['GET'])
def player_data(request, format=None):

    if request.method == 'GET':
        try:
            player_id = request.GET["player_id"]
            player = Players.objects.get(pk=player_id)
            serializer = PlayersSerializer(player, many=False)
            return Response(serializer.data)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'user_found': False
            }, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        player_id = request.GET["player_id"]
        player = Players.objects.get(pk=player_id)
        player.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def lobby_info(request, format=None):

    if request.method == "GET":
        try:
            game_id = request.GET['game_id']
            lobby = Lobby.objects.filter(game=Game.objects.get(id=game_id))
            serializer = LobbySerializer(lobby, many=True)
            return Response(serializer.data)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'lobby_found':False
            }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def lobby_row_info(request, format=None):

    if request.method == "GET":
        try:
            lobby_id = request.GET['lobby_id']
            lobby = Lobby.objects.get(pk=lobby_id)
            serializer = LobbySerializer(lobby, many=False)
            return Response(serializer.data)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'lobby_found': False
            }, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def game_info(request, format=None):

    if request.method == "GET":
        try:
            game_id = request.GET['game_id']
            game = Game.objects.get(pk=game_id)
            serializer = GameSerializer(game, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'game_found': False
            }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def invite_info(request, format=None):

    if request.method == "GET":
        try:
            invite_id = request.GET['invite_id']
            invite = Invite.objects.get(pk=invite_id)
            serializer = InviteSerializer(invite, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'game_found': False
            }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_invites(request, format=None):

    if request.method == "GET":
        try:
            invites = Invite.objects.filter(receiver=request.GET["receiver"])
            serializer = InviteSerializer(invites, many=True)
            return Response(serializer.data)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'invites_found': False
            }, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({
            'invites_retrieved':False
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def teams(request, format=None):

    if request.method == "GET":
        try:
            lobby_id = request.GET['lobby_id']
            teams = Teams.objects.get(lobby=Game.objects.get(pk=lobby_id))
            serializer = TeamsSerializer(teams, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'teams_found': False
            }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_game_tags_player(request, format=None):

    if request.method == "GET":
        try:
            game_id = request.GET['game_id']
            player_id = request.GET['player_id']
            game = Game.objects.get(pk=game_id)
            tags = Tag.objects.filter(game = game).filter(sender_id=player_id)
            serializer = TagSerializer(tags,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_games_list(request, format=None):

    if request.method == "GET":
        try:
            latitude = request.GET['latitude']
            longitude = request.GET['longitude']
            games = Game.objects.filter(latitude__range=(latitude-0.1,latitude+0.1)).filter(longitude__range=(longitude-0.1,longitude+0.1))
            serializer = GameSerializer(games,many=True)
            return Response(serializer.data)
        except Exception as e:
            pprint.pprint(e)
            return Response(
                {
                    'list_games_found':False
                }, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(
            {
                'list_games_found': False
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def start_game(request, format=None):

    if request.GET:
        try:
            game_id = request.GET['game_id']
            game_to_play = Game.objects.get(pk=game_id)
            lobby = Lobby.objects.filter(game=game_to_play).filter(kicked=False).filter(in_game=True)
            if len(lobby) >= 2:
                game_to_play.game_status = 1002
                game_to_play.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({
                    'error_message': "You need to have more than 2 players ready to start the game!"
                }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'game_started':False
            },status.HTTP_400_BAD_REQUEST)


# ---
#  Active references
# ---


@csrf_exempt
@api_view(['POST'])
def player_login(request, format=None):

    if request.POST:
        try:
            player = Players.objects.get(email=request.POST.get('email'))
            if player.password == request.POST.get('password'):
                request.session['user_logged'] = player.id
                request.session['user_pseudo'] = player.pseudoname
                request.session.set_expiry(7200)
                return Response({
                    'login_result': True,
                    'player_id': player.id
                }, status=status.HTTP_200_OK)
            login_note = "Wrong username or password"
            return Response({
                'login_result': False,
                'error_message': login_note
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'login_result':False,
                'error_message': "An unexpected error occured"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        Response({
            'login_result':False,
            'error_message': "Unauthorized access"
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def player_logout(request, format=None):
    try:
        del request.session["user_logged"]
        return Response(status=status.HTTP_204_NO_CONTENT)
    except KeyError:
        return Response({
            'logout_result': False,
            'logout_message': "Error while logging out"
        }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def send_invite(request, format=None):

    if request.POST:
        try:
            receiver_name = request.POST['receiver_name']
            game_id = request.POST['game_id']
            player = Players.objects.get(pseudoname=receiver_name)
            invitation = Invite()
            invitation.game = Game.objects.get(pk=game_id)
            invitation.sender = request.POST["sender_id"]
            sender = Players.objects.get(pk=invitation.sender)
            invitation.receiver = player.id
            invitation.save()

            # Now we send an email to the user to confirm his email

            sendemail("jobmarketapp@gmail.com",
                      [player.email],
                      [],
                      "TAG: You have an invitation from "+str(sender.pseudoname)+"!",
                      "The player "+str(sender.pseudoname)+" invited you to his game. Jump in right now",
                      "jobmarketapp@gmail.com",
                      "jobmarketapp426750")

            return Response({
                "player_registration_result": True
            }, status=status.HTTP_201_CREATED)
        except Exception as e:

            pprint.pprint(e)

            return Response(
                {
                    "player_registration_result": False,
                }, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {
                "player_registration_result": False,
            }, status=status.HTTP_400_BAD_REQUEST
        )

@csrf_exempt
@api_view(['POST'])
def add_to_lobby(request, format=None):

    if request.POST:
        player_id = request.POST['player_id']
        game_id = request.POST['game_id']
        game = Game.objects.get(pk = game_id)
        lobby = Lobby.objects.get(game=game)
        invite = Invite.objects.filter(lobby=lobby).filter(receiver=player_id)
        if game.private:

            if invite is not None and invite.receiver == player_id:
                new_lobby_in = Lobby()
                new_lobby_in.player = Players.objects.get(pk=player_id)
                new_lobby_in.game = game
                new_lobby_in.in_game = False
                new_lobby_in.admin = False
                new_lobby_in.save()
                return Response(
                    {
                        "lobby_add": True,
                    }, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "lobby_add": False,
                    }, status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            new_lobby_in = Lobby()
            new_lobby_in.player = Players.objects.get(pk=player_id)
            new_lobby_in.game = game
            new_lobby_in.in_game = False
            new_lobby_in.admin = False
            new_lobby_in.save()
            return Response(
                {
                    "lobby_add": True,
                }, status=status.HTTP_201_CREATED
            )
    else:
        return Response(
            {
                "lobby_add": False,
            }, status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(['POST'])
def kick_from_lobby(request, format=None):

    if request.POST:
        try:
            lobby_id = request.POST['lobby_id']
            player_to_kick = Lobby.objects.get(pk=lobby_id)
            player_to_kick.kicked = True
            player_to_kick.time_kicked = datetime.now()
            player_to_kick.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'kicked':False
            }, status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
def register_player(request, format=None):

    if request.POST:
        player = Players()

        player.name = request.POST.get('name')
        player.pseudoname = request.POST.get('pseudoname')
        player.email = request.POST.get('email')
        player.password = encrypt(password_encrypt, request.POST.get("password").encode('utf8'))
        player.phone_number = request.POST.get("phone_number")
        player.date_creation = timezone.now()
        player.birthday = request.POST.get("birthday")
        player.user_log_ip = get_client_ip(request)

        try:
            if request.POST.get('password') == request.POST.get("password_confirm"):
                delta = datetime.now() - datetime.strptime(str(player.birthday), date_format)
                if delta.days >= valid_days_limit:
                    player.save()
                else:
                    raise Exception("User too young to be registered")
            else:
                return Response({
                    'player_registration_result': False,
                    'error_message': "The passwords do not match!"
                })

            # Now we send an email to the user to confirm his email

            sendemail("jobmarketapp@gmail.com",
                      [player.email],
                      [],
                      "Successful Signup",
                      "Your account has been successfully setup. It is time to play!",
                      "jobmarketapp@gmail.com",
                      "jobmarketapp426750")

            return Response({
                "player_registration_result": True
            })

        except Exception as e:
            error_message = str(e)
            pprint.pprint(error_message)
            return Response({
                    'player_registration_result':False,
                    'error_message':"Unexpected Error Occured"
                })
    else:
        return Response({
            'player_registration_result': False,
            'error_message': "Unauthorized Action"
        })


@csrf_exempt
@api_view(['POST'])
def create_game(request, format=None):

    if request.POST:
        try:
            game_admin = Players.objects.get(pk=request.POST['player_id'])

            new_game = Game()
            new_lobby = Lobby()     # Each new game will create a new lobby linked to it

            new_game.game_name = request.POST.get("game_name")
            new_game.type_game = request.POST.get("type_game")
            new_game.duration = request.POST.get("game_duration")
            new_game.game_status = request.POST.get("game_status")

            new_game.private = True
            if request.POST.get("private") == "false":
                new_game.private = False

            new_game.longitude = request.POST.get("longitude")
            new_game.latitude = request.POST.get("latitude")
            new_game.save()

            new_lobby.game = Game.objects.get(pk=new_game.pk)
            new_lobby.player = game_admin
            new_lobby.creation_time = timezone.now()
            new_lobby.in_game = False
            new_lobby.admin = True
            new_lobby.save()

            serializer = GameSerializer(new_game, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            pprint.pprint(e.with_traceback())
            return Response({
                'game_created': False,
                'error_message': "Unexpected Error Occured!"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'player_registration_result': False,
            'error_message': "Unauthorized Action"
        }, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@api_view(['POST'])
def player_ready(request, format=None):

    if request.POST:
        try:
            lobby_index = request.POST['lobby_index']
            player_in_game = Lobby.objects.get(pk=lobby_index)
            player_in_game.in_game = True
            player_in_game.save()
            return Response({
                'player_ready':True
            },status=status.HTTP_200_OK)
        except Exception as e:
            pprint.pprint(e)
            return Response({
                'player_ready':False
            },status=status.HTTP_400_BAD_REQUEST)


# ---
# Other functions
# ---


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    message = header + message

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(login, password)
    server.sendmail(from_addr, to_addr_list, message)
    server.close()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip