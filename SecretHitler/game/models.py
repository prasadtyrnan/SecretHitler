from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from numpy import random as rand
import random
# Create your models here.

class Lobby(models.Model):
    room_num = models.IntegerField(primary_key=True)
    num_players = models.IntegerField(default=0)
    player_one = models.CharField(max_length=100, default="")
    player_two = models.CharField(max_length=100, default="")
    player_three = models.CharField(max_length=100, default="")
    player_four = models.CharField(max_length=100, default="")
    player_five = models.CharField(max_length=100, default="")
    player_six = models.CharField(max_length=100, default="")
    player_seven = models.CharField(max_length=100, default="")
    player_eight = models.CharField(max_length=100, default="")
    player_nine = models.CharField(max_length=100, default="")
    player_ten = models.CharField(max_length=100, default="")
    game_started = models.BooleanField(default=False)
    fascist_one = models.CharField(max_length=100, default="")
    fascist_two = models.CharField(max_length=100, default="")
    fascist_three = models.CharField(max_length=100, default="")
    hitler = models.CharField(max_length=100, default="")
    deck = models.CharField(max_length=17, default="FFFFFFFFFFFLLLLLL")
    discards = models.CharField(max_length=17, default="")
    held_cards = models.CharField(max_length=3, default="")
    president = models.CharField(max_length=100, default="")
    president_index = models.IntegerField(default=0)
    chancellor = models.CharField(max_length=100, default="")
    previous_president = models.CharField(max_length=100, default="")
    previous_chancellor = models.CharField(max_length=100, default="")
    state = models.IntegerField(default=0)
    ready = models.CharField(max_length=10, default="")
    fascist_count = models.IntegerField(default=0)
    liberal_count = models.IntegerField(default=0)
    hidden_info = models.CharField(max_length=100, default="")
    failed_governments = models.IntegerField(default=0)
    veto_done = models.BooleanField(default=False)

    def get_card1(self):
        if self.held_cards[0] == "F":
            return "Fascist"
        else:
            return "Liberal"

    def get_card2(self):
        if self.held_cards[1] == "F":
            return "Fascist"
        else:
            return "Liberal"

    def get_card3(self):
        if self.held_cards[2] == "F":
            return "Fascist"
        else:
            return "Liberal"

    def draw_cards(self):
        self.prep_deck()
        self.held_cards = self.deck[:3]
        self.deck = self.deck[3:]
        print(self.held_cards)
        print(self.deck)

    def discard(self, index):
        self.discards = self.discards + self.held_cards[index]
        self.held_cards = self.held_cards[0:index] + self.held_cards[index+1:len(self.held_cards)]
        if self.held_cards == 'F':
            self.fascist_count += 1
        elif self.held_cards == 'L':
            self.liberal_count += 1

    def reset_ready(self):
        self.ready = ""
        for i in range(0, self.num_players):
           self.ready += "i"
        for i in range(self.num_players, 10):
            self.ready += "-"

    def is_ready(self):
        for i in range(0, self.num_players):
            if self.ready[i] == "i":
                return False
        return True

    def vote_nein(self, user):
        for i in range(self.num_players):
            if self.get_players()[i] == user:
                self.ready = self.ready[0:i] + 'n' + self.ready[i+1:10]

    def vote_ja(self, user):
        for i in range(self.num_players):
            if self.get_players()[i] == user:
                self.ready = self.ready[0:i] + 'j' + self.ready[i+1:10]

    def vote_abstain(self, user):
        for i in range(self.num_players):
            if self.get_players()[i] == user:
                self.ready = self.ready[0:i] + 'a' + self.ready[i+1:10]

    def motion_passes(self):
        ja_count = 0
        nein_count = 0
        for i in range(self.num_players):
            if self.ready[i] == 'n':
                nein_count += 1
            elif self.ready[i] == 'j':
                ja_count += 1
        return ja_count > nein_count

    def advance_game(self):
        if(self.state == 0):
            self.state = 1
            self.reset_ready()
        elif(self.state == 1):
            if self.chancellor != "":
                self.state = 2
        elif(self.state == 2):
            if self.ready.find("*") == -1:
                if(self.motion_passes()):
                    self.state = 3
                    self.draw_cards()
                    self.veto_done = False
                    if(self.chancellor == self.hitler and self.fascist_count > 2):
                        self.state = 5
                else:
                    self.move_president()
                    self.failed_governments += 1
                    if(self.failed_governments == 3):
                        self.failed_governments = 0
                        if(self.deck[0] == 'F'):
                            self.fascist_count += 1
                        else:
                            self.liberal_count += 1
                        self.deck = self.deck[1:]
                    self.state = 1
                self.reset_ready()
        elif(self.state == 3):
            if len(self.held_cards) == 2:
                self.state = 4
        elif(self.state == 4):
            if len(self.held_cards) == 1:
                self.state = 1
                if(self.fascist_count == 6):
                    self.state = 5
                elif(self.liberal_count == 5):
                    self.state = 6
                if(self.held_cards == 'F'):
                    if(self.fascist_count == 5 or self.fascist_count == 4):
                        self.state = 7
                    elif self.num_players == 9 or self.num_players == 10:
                        if self.fascist_count == 1 or self.fascist_count == 2:
                            self.state = 8
                        elif self.fascist_count == 3:
                            self.state = 9
                    elif self.num_players == 7 or self.num_players == 8:
                        if self.fascist_count == 2:
                            self.state = 8
                        elif self.fascist_count == 3:
                            self.state = 9
                    elif self.num_players == 5 or self.num_players == 6:
                        if self.fascist_count == 3:
                            self.state = 10
                            self.prep_deck()
                            if(self.deck[0] == "F"):
                                self.hidden_info = "Fascist, "
                            else:
                                self.hidden_info = "Liberal, "
                            if(self.deck[1] == "F"):
                                self.hidden_info += "Fascist, and "
                            else:
                                self.hidden_info += "Liberal, and "
                            if(self.deck[2] == "F"):
                                self.hidden_info += "Fascist"
                            else:
                                self.hidden_info += "Liberal"
                    else:
                        self.move_president()
                else:
                    self.move_president()
        elif(self.state == 7):
            if(self.hitler == ""):
                self.state = 6
            else:
                self.state = 1
                self.reset_ready()
                self.move_president()
        elif self.state == 8:
            self.state = 11
        elif self.state == 9:
            self.state = 1
        elif(self.state == 10):
            self.state = 1
            self.move_president()
        elif self.state == 11:
            self.state = 1
            self.move_president()

    def ready_up(self, user):
        for i in range(self.num_players):
            if self.get_players()[i] == user:
                self.ready = self.ready[0:i] + 'y' + self.ready[i+1:10]
                print(self.ready)

    def valid_chancellors(self):
        output = []
        for player in self.get_players():
            if player != self.president:
                if self.num_players < 7:
                    output.append(player)
                else:
                    if player != self.previous_president and player != self.previous_chancellor:
                        output.append(player)
        return output

    def move_president(self):
        self.previous_president = self.president
        self.previous_chancellor = self.chancellor
        self.president_index = (self.president_index + 1) % len(self.get_players())
        self.president = self.get_players()[self.president_index]

    def prep_deck(self):
        if len(self.deck) < 3:
            self.deck += self.discards
            self.shuffle_deck()

    def shuffle_deck(self):
        self.deck = ''.join(random.sample(self.deck, len(self.deck)))

    def get_fascists(self):
        output = []
        if self.fascist_one != "":
            output.append(self.fascist_one)
            if self.fascist_two != "":
                output.append(self.fascist_two)
                if self.fascist_three != "":
                    output.append(self.fascist_three)
        return output

    def add_fascist(self, user):
        if self.fascist_one == "":
            self.fascist_one = user
        elif self.fascist_two == "":
            self.fascist_two = user
        elif self.fascist_three == "":
            self.fascist_three = user

    def clear_fascists(self):
        self.fascist_one = ""
        self.fascist_two = ""
        self.fascist_three = ""

    def start_game(self):
        self.deck = "FFFFFFFFFFFLLLLLL"
        self.hidden_info = ""
        self.discards = ""
        self.held_cards = ""
        self.clear_fascists()
        self.state = 0
        self.chancellor = ""
        self.previous_chancellor = ""
        self.previous_president = ""
        self.fascist_count = 5
        self.liberal_count = 0
        self.president_index = 0
        if self.num_players > 4:
            print('Starting Game')
            players = self.get_players()
            num_fascists = 1
            if self.num_players == 7 or self.num_players == 8:
                num_fascists = 2
            if self.num_players == 9 or self.num_players == 10:
                num_fascists = 3
            index = rand.randint(0, len(players)-1)
            self.hitler = players[index]
            del players[index]
            for i in range(0, num_fascists):
                index = rand.randint(0, len(players)-1)
                self.add_fascist(players[index])
                del players[index]
            self.president = self.get_players()[0]
            self.game_started = True
            self.shuffle_deck()
            self.reset_ready()
            # DELETE THIS LINE!
            self.ready = "rrrrrrrrrr"

    def get_players(self):
        output = []
        if self.num_players > 0:
            output.append(self.player_one)
        if self.num_players > 1:
            output.append(self.player_two)
        if self.num_players > 2:
            output.append(self.player_three)
        if self.num_players > 3:
            output.append(self.player_four)
        if self.num_players > 4:
            output.append(self.player_five)
        if self.num_players > 5:
            output.append(self.player_six)
        if self.num_players > 6:
            output.append(self.player_seven)
        if self.num_players > 7:
            output.append(self.player_eight)
        if self.num_players > 8:
            output.append(self.player_nine)
        if self.num_players > 9:
            output.append(self.player_ten)
        return output

    def kill_player(self, user):
        if user == self.hitler:
            self.hitler = ""
        players = self.get_players()
        self.player_one = ""
        self.player_two = ""
        self.player_three = ""
        self.player_four = ""
        self.player_five = ""
        self.player_six = ""
        self.player_seven = ""
        self.player_eight = ""
        self.player_nine = ""
        self.player_ten = ""
        self.num_players = 0
        for player in players:
            if player != user:
                self.add_player(player)

    def is_room_left(self):
        return self.num_players < 10

    def add_player(self, player):
        if player not in self.get_players():
            if self.num_players == 0:
                self.player_one = player
                self.num_players += 1
            elif self.num_players == 1:
                self.player_two = player
                self.num_players += 1
            elif self.num_players == 2:
                self.player_three = player
                self.num_players += 1
            elif self.num_players == 3:
                self.player_four = player
                self.num_players += 1
            elif self.num_players == 4:
                self.player_five = player
                self.num_players += 1
            elif self.num_players == 5:
                self.player_six = player
                self.num_players += 1
            elif self.num_players == 6:
                self.player_seven = player
                self.num_players += 1
            elif self.num_players == 7:
                self.player_eight = player
                self.num_players += 1
            elif self.num_players == 8:
                self.player_nine = player
                self.num_players += 1
            elif self.num_players == 9:
                self.player_ten = player
                self.num_players += 1

    def investigate(self, user):
        for player in self.get_players():
            if player == user:
                if player in self.get_fascists():
                    self.hidden_info = "Fascist"
                elif player == self.hitler:
                    self.hidden_info = "Fascist"
                else:
                    self.hidden_info = "Liberal"

    def __str__(self):
        return str(self.room_num)

    def get_absolute_url(self):
        return reverse('lobby', kwargs={'pk': self.room_num})
