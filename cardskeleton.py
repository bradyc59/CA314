import itertools
import random

class Card(object):
    def __init__(self,suit,value):
        self.value = value
        self.suit = suit
    
    def compare(self, Card):
        '''will be used to determine the best possible hand for the player
            and will require an algorithm that iterates through each possible combination of 5 card sets
            possible for a player to determine their best hand'''

class Deck(object):
    def __init__(self):
        self.cards=[]
        self.build()
    
    def build(self):
        suit = [1, 2, 3, 4] #Hearts = 1, Diamonds = 2, Spades = 3, Clubs = 4
        for s in suit:
            for v in range(1,14):
                self.cards.append(Card(v, s))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
        print("--Deck Shuffled--")

    def deal(self, location, times=1):
            for i in range(times):
                location.cards.append(self.pop(0))

    def burn(self):
            self.pop(0)

    def flop(self):
        self.burn()
        self.deal(self, 3)
    
    def river(self):
        self.burn()
        self.deal(self, 1)

    def run(self):
        self.burn()
        self.deal(self, 1)
    
    def resetDeck(self):
        self.cards=[]
        suit = [1, 2, 3, 4] #Hearts = 1, Diamonds = 2, Spades = 3, Clubs = 4
        for s in suit:
            for v in range(1,14):
                self.cards.append(Card(v, s))

class Player(object):
    def __init__(self, name, hand):
        self.name = name
        self.chips = 0
        self.bet = 0
        self.in_play = False
        self.hand = hand
        self.ready = False
        self.fold = False
        self.check = False
        self.allIn = False

    
    def raise_bet(self):
        pass

    def check(self):
        '''which will allow a player to bet 0 for the round but can only be carried out if every previous
           player has checked,'''

    def fold(self):
        '''allows the player to sit out for the entire hand of the poker
           game but they cannot win that round and their previous bets are still in the pot for that hand,'''
    
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

class Hand(object):
    def __init__(self):
        self.hand=[]
    
    def myHand(self):
        card = Card.drawCard()
        self.hand.append(card)

    def compare(self, Hand):
        '''used in other classes and is used to determine the highest
           value 5 cards for each player at the end of the hand of poker. It is also used to compare one
           players 5 cards against others and determine a winner i.e whoever has the highest integer
           after the comparison.'''

class PokerGame(object):
    def __init__(self):
        self.currentPlayer = 0
        self.currentDealer = 0
        self.currentSmallBlind = 0
        self.currentBigBlind = 0
        self.round = 0
        self.pot = 0
    
    def playRound(self):
        '''which will commence the round of poker at the start of the game and after each
           round of poker has ended this will also include the count to increase the amount of rounds
           played'''
    
    def winner(self):
        '''will pay the pot into the winners remaining
           chip balance.'''

class GameSettings(object):
    def __init__(self):
        self.confirmed = False
    
    def players(self):
        '''allows the person who creates the game
           to set the amount of players,'''
    
    def startingChips(self):
        '''has a type integer and is used to set the
           amount of chips each player has at the start of the game.'''
    
    def blinds(self):
        '''which is an integer type
           and is set by the user to determine the cost of Small and Big Blinds,'''

    def AIDifficulty(self):
        '''allows a user to set an integer value for AI difficulty in the range of 1-10 where 1 is the
           easiest and 10 is the hardest.'''