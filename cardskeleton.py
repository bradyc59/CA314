import itertools
import random
import numpy as np

class Card(object):
    def __init__(self,suit,value, faceup=True):
        self.value = value
        self.suit = suit
        self.faceup = faceup
    
    def compare(self, Card):
        '''will be used to determine the best possible hand for the player
            and will require an algorithm that iterates through each possible combination of 5 card sets
            possible for a player to determine their best hand'''


    def to_suit(self):
        if self.suit == 1:
            self.suit = "Hearts"
        elif self.suit == 2:
            self.suit = "Diamonds"
        elif self.suit == 3:
            self.suit = "Spades"
        elif self.suit == 4:
            self.suit = "Clubs"

        return self.suit


    def __str__(self):
        if self.faceup:

            return str(self.suit) + str(self.value)
        else:
            return "XX"

class Hand(object):

    def __init__(self, name, PokerGame):
        self.hand= []
        self.community_cards = []
        self.cards = []
        self.total_cards = (self.cards + self.community_cards)
        PokerGame.Players.append(self)
        self.name = name

        Hand.position += 1
        self.position = Hand.position
        self.small_blind = False
        self.big_blind = False
        self.dealer = False
        self.is_folded = False
        self.stack = 1000
        self.hand_value = 0

    @property

    def get_position(self):

        return self.position%PokerGame.players_at_table

    def compare(self, Hand):
        '''used in other classes and is used to determine the highest
           value 5 cards for each player at the end of the hand of poker. It is also used to compare one
           players 5 cards against others and determine a winner i.e whoever has the highest integer
           after the comparison.'''


class Deck(Hand):

    def __init__(self):
        self.cards = []
        self.build()


    def build(self):
        suit = [1, 2, 3, 4] #Hearts = 1, Diamonds = 2, Spades = 3, Clubs = 4
        for s in suit:
            for v in range(1,14):
                self.cards.append(Card(v, s))
        self.cards.shuffle()
        return self.cards

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
        print("--Deck Shuffled--")
        return self.cards


    def deal(self, PokerGame):
        if Pot.current_street == 'pre-flop':
            for player in PokerGame.players:
                self.hand.append(self.cards.pop())
            for player in PokerGame.players:
                self.hand.append(self.cards.pop())
        elif Pot.current_street == 'flop':
            self.burn()
            self.community_cards.append(self.cards.pop())
            self.community_cards.append(self.cards.pop())
            self.community_cards.append(self.cards.pop())
        elif Pot.current_street == 'post-flop':
            self.burn()
            self.community_cards.append(self.cards.pop())
        elif Pot.current_street == 'turn':
            self.burn()
            self.community_cards.append(self.cards.pop())


    def suits_to_string(self):
        if self.suit == 1:
            self.suit = "Hearts"
        elif self.suit == 2:
            self.suit = "Diamonds"
        elif self.suit == 3:
            self.suit = "Spades"
        elif self.suit == 4:
            self.suit = "Clubs"


    def burn(self):
        self.cards.pop(0)


    def flop(self):
        return self.deal(self)


    def river(self):
        return self.deal(self)


    def run(self):
        return self.deal(self)


    def resetDeck(self):
        self.cards=[]
        suit = [1, 2, 3, 4] #Hearts = 1, Diamonds = 2, Spades = 3, Clubs = 4
        for s in suit:
            for v in range(1,14):
                self.cards.append(Card(v, s))
        self.cards.shuffle()
        return self.cards

class Player(object):

    def __init__(self, name, hand):
        self.name = name
        self.chips = 0
        self.bet = 0
        self.in_play = True
        self.hand = hand
        self.ready = False
        self.fold = False
        self.check = False
        self.allIn = False
        self.street = 0

    def raise_bet(self):

        pass

    def check(self):
        '''which will allow a player to bet 0 for the round but can only be carried out if every previous
           player has checked,'''

    def fold(self):
        self.fold = True
        self.in_play = False
        self.bet = 0
        self.street = 0

        print(str(self.name) + "folds")

    
    def call(self):
        '''allows player to match bet of previous player'''
    
    def allIn(self):
        ''' allows player to put in all remaining chips they have as a bet'''

class AIPlayer(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
    
    def performAction(self):
        '''will allow the AI to
           perform actions like a human player and use an algorithm to decide the action and will also
           take into account the difficulty set.'''


class PokerGame(Hand):

    def __init__(self):
        self.Players = []
        self.currentPlayer = 0
        self.currentDealer = 0
        self.currentSmallBlind = GameSettings.small_blind
        self.currentBigBlind = GameSettings.big_blind
        self.round = 0
        self.pot = 0
        self.cards = []

    def next_hand(Deck, Hand):
        Hand.cards.clear()
        Deck.cards.clear()

    def players_at_table(self):

        return len(self.Players)

    def playRound(self, GameSettings):
        GameSettings.players()
        GameSettings.small_blind()
        GameSettings.big_blind()
        GameSettings.AIDifficulty()
        GameSettings.startingChips()
        """ We need to add more function calls and flow control to judge the running of a round in poker the finishing 
        of this will be clearing the majority of the lists that contain hands and the deck"""
    
    def winner(self):
        '''will pay the pot into the winners remaining
           chip balance.'''

    def best_hands(hand_list, n):
        arr = np.asarray(list)
        x = np.dtype([('', arr.dtype)]*n)
        result = np.fromiter(itertools.combinations(arr, n), x)
        return result.view(arr.dtype).reshape(-1, n)

class Pot(Hand):
    pot_number = 0

    def __init__(self, name):
        self.players = []
        self.activeplayers =[]
        self.foldedplayers = []
        self.name = name
        self.small_blind = GameSettings.small_blind
        self.big_blind = GameSettings.big_blind

    def current_street(Hand):
        if len(Hand.community_cards) == 0 and len(Hand.cards) == 52:
            current_street = 'pre-flop'
            return current_street
        elif len(Hand.community_cards) == 0 and len(Hand.cards) != 52:
            current_street = 'flop'
            return current_street
        elif len(Hand.community_cards) == 3:
            current_street = 'post-flop'
            return current_street
        elif len(Hand.community_cards) == 4:
            current_street = 'turn'
            return current_street
        elif len(Hand.community_cards) == 5:
            current_street = 'river'
            return current_street


class GameSettings(object):

    def __init__(self):
        self.confirmed = False
    
    def players(self):
        players = int(input("How many Players?"))
        if players > 6:
                print("Error cannot have more than 6 players")
                GameSettings.players(self)
        else:
            return players

    def startingChips(self):
        return int(input("How many chips for each player at the start?"))

    def small_blind(self):
        small_blind = int(input("How much would you like small blinds to cost"))
        return small_blind

    def big_blind(self):
        big_blind = int(input("How much would you like big blinds to cost"))
        if big_blind != 2 * GameSettings.small_blind:
            print("Error Big blind must be double small blind")
            GameSettings.big_blind(self)
        else:
            return big_blind

    def AIDifficulty(self):
        AIdifficulty = int(input("What difficulty would you like to set AI at?"))
        if AIdifficulty > 10 or AIdifficulty < 1:
            print("Error AI difficulty must be an integer less than 10 and greater than 0")
            GameSettings.AIDifficulty(self)
        else:
            return AIdifficulty
