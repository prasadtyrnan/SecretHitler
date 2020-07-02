from django.shortcuts import render, get_object_or_404, redirect
from .models import Lobby
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request, 'game/home.html')

class LobbyCreateView(CreateView):
    model = Lobby
    fields = ['room_num']

def lobby_connect(request):
    if(request.GET.get('connect')):
        print(request.GET.get('room_num'))
        return redirect('/lobby/' + str(request.GET.get('room_num')) + "/player")
    return render(request, 'game/lobby_connect.html')

def custom_lobby_detail_view(request, pk):
    lobby = get_object_or_404(Lobby, room_num=pk)
    if(lobby.game_started):
        if(request.GET.get('gameunstart')):
            lobby.game_started = False
            lobby.save()
            return HttpResponseRedirect(request.path_info)
        if(lobby.is_ready()):
            lobby.advance_game()
            lobby.save()
        return render(request, 'game/lobby_detail_game.html', context={'object':lobby})
    else:
        if(request.GET.get('gamestart')):
            lobby.start_game()
            lobby.save()
            print(lobby.game_started)
            return HttpResponseRedirect(request.path_info)
        return render(request, 'game/lobby_detail.html', context={'object':lobby})


class LobbyDeleteView(DeleteView):
    model = Lobby
    success_url = "/"

@login_required
def custom_player_detail(request, pk):
    lobby = get_object_or_404(Lobby, room_num=pk)
    if(lobby.game_started):
        isSmallGame = (lobby.num_players < 7)

        if request.user.username in lobby.get_players():
            if request.GET.get('ready'):
                print(request.user.username + ' readying up')
                lobby.ready_up(request.user.username)
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('nominate'):
                lobby.chancellor = request.GET.get('nominate')
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('shoot'):
                print("BANG! " + request.GET.get('shoot') + " has been shot!")
                lobby.kill_player(request.GET.get('shoot'))
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('ja'):
                lobby.vote_ja(request.user.username)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('nein'):
                print('nein')
                lobby.vote_nein(request.user.username)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('abstain'):
                lobby.vote_abstain(request.user.username)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('discard1'):
                lobby.discard(0)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('discard2'):
                lobby.discard(1)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('discard3'):
                lobby.discard(2)
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('investigate'):
                lobby.investigate(request.GET.get('investigate'))
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('peeked'):
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('appoint'):
                lobby.previous_president = request.user.username
                lobby.previous_chancellor = lobby.chancellor
                lobby.president = request.GET.get('appoint')
                lobby.advance_game()
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('veto'):
                lobby.state = 12
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('approve_veto'):
                lobby.move_president()
                lobby.state = 1
                lobby.discards = lobby.discards + lobby.held_cards
                lobby.held_cards = ""
                lobby.failed_governments += 1
                if (lobby.failed_governments == 3):
                    lobby.failed_governments = 0
                    if (lobby.deck[0] == 'F'):
                        lobby.fascist_count += 1
                    else:
                        lobby.liberal_count += 1
                    lobby.deck = lobby.deck[1:]
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            if request.GET.get('reject_veto'):
                lobby.veto_done = True
                lobby.state = 4
                lobby.save()
                return HttpResponseRedirect(request.path_info)

            context={'object': lobby, 'smallGame': isSmallGame}

            if lobby.state == 0:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_hitler_state0.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state0.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state0.html', context=context)
            elif lobby.state == 1:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state1.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state1.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state1.html', context=context)
            elif lobby.state == 2:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state2.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state2.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state2.html', context=context)
            elif lobby.state == 3:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state3.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state3.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state3.html', context=context)
            elif lobby.state == 4:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state4.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state4.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state4.html', context=context)
            elif lobby.state == 5:
                return render(request, 'game/player_fascistswin.html', context=context)
            elif lobby.state == 6:
                return render(request, 'game/player_liberalswin.html', context=context)
            elif lobby.state == 7:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state7.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state7.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state7.html', context=context)
            elif lobby.state == 8:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state8.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state8.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state8.html', context=context)
            elif lobby.state == 9:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state9.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state9.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state9.html', context=context)
            elif lobby.state == 10:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state10.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state10.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state10.html', context=context)
            elif lobby.state == 11:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state11.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state11.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state11.html', context=context)
            elif lobby.state == 12:
                if request.user.username == lobby.hitler:
                    return render(request, 'game/player_game_fascist_state12.html', context=context)
                elif request.user.username in lobby.get_fascists():
                    return render(request, 'game/player_game_fascist_state12.html', context=context)
                else:
                    return render(request, 'game/player_game_liberal_state12.html', context=context)
            else:
                return render(request, 'game/player_no_join.html')
        else:
            return render(request, 'game/player_no_join.html', context={'object':lobby})
    else:
        if(request.user.username in lobby.get_players()):
            return render(request, 'game/player_lobby_detail.html', context={'object':lobby})
        else:
            if(lobby.is_room_left()):
                lobby.add_player(request.user.username)
                lobby.save()
                return render(request, 'game/player_lobby_detail.html', context={'object':lobby})
            else:
                return render(request, 'game/player_no_join.html', context={'object':lobby})