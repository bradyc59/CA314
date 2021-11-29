import socket
from _thread import *
from queue import Queue

HOST = '127.0.0.1'
PORT = 51040

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.connect((HOST,PORT))
print("connected to server: ", HOST)

def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(20).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

serverMsg = Queue(20)
start_new_thread(handleServerMsg, (server, serverMsg))

import pygame, random
from player import Player
from load_images import *
from game_control import *
from draw_game import *
from draw_splash import *


class PokerGame(object):

    def init(self, server, numPlayers=4):
        self.whoAmI = 0
        self.server = server
        self.otherStrangers = 0
        self.pokerMove = None

        self.screen = 'splash'
        self.timerDelay = 0; self.tickSpeed = 10
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.players = [Player(i) for i in range(numPlayers)]
        self.boardImage = getBoardImage(self.width, self.height)
        self.statusBoardImage = getStatusBoardImage(self, 4)
        self.cardScale = 30
        self.cardImages = getCardImages(self.cardScale)
        self.drawPlayerPositions = getDrawPlayerPositions(self,numPlayers)
        self.buttonImages = getButtonImages()
        self.status = GameController(numPlayers, self.players)
        self.buttonPositions = dict()

        self.status.server = self.server
        self.status.firstClick = False

    def mousePressed(self, x, y):
        if self.screen == 'splash':
            if self.status.isInBounds(self.startButtons,'start-game',x,y):
                self.screen = 'game'
                self.pokerMove = 'newgame'
                print('sending', self.pokerMove)
                self.server.send((self.pokerMove +'\n').encode())
        elif self.status.gameOver==False and self.screen == 'game' and\
        self.whoAmI == self.status.currentPlayer:
            if self.status.isInBounds(self.buttonPositions,'check-call',x,y):
                self.pokerMove = 'turn_check/call_0'
                print('sending', self.pokerMove)
                self.server.send((self.pokerMove +'\n').encode())
                if self.status.firstClick == False:
                    self.status.firstClick = True
            elif self.status.isInBounds(self.buttonPositions,'fold',x,y):
                self.pokerMove = 'turn_fold_0'
                print('sending', self.pokerMove)
                self.server.send((self.pokerMove +'\n').encode())
            elif self.status.isInBounds(self.buttonPositions,'raise',x,y):
                self.pokerMove = 'turn_raise_%d' % self.status.tempBet
                print('sending', self.pokerMove)
                self.server.send((self.pokerMove +'\n').encode())
            elif self.status.isInBounds(self.buttonPositions,'end-game',x,y)\
            and self.status.firstClick == True:
                self.screen = 'gameOver'
                self.status.getWinner(self.players)
                self.pokerMove = 'endGame'
                print('sending', self.pokerMove)
                self.server.send((self.pokerMove +'\n').encode())

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            msg = msg.strip(); msg = msg.split('_')
            
            print('msg recv:', msg)

            def decodeHands(encoded):
                def decodeSuit(s):
                    if   s == 'd': return 'diamonds'
                    elif s == 's': return 'spades'
                    elif s == 'h': return 'hearts'
                    else:          return 'clubs'
                def decodeValue(n):
                    if n == 'j':          return 'jack'
                    elif n == 'q':        return 'queen'
                    elif n == 'k':        return 'king'
                    elif n == 'a':        return 'ace'
                    elif n in '23456789': return n
                    else:                 return '10'
                
                cards = encoded.split(',')
                cards = cards[:-1]

                print('cards', cards)
                result = []
                for card in cards:
                    if len(card) == 2:
                        suit, value = decodeSuit(card[0]),decodeValue(card[1])
                        result.append((suit, value))
                return result

            pID = int(msg[-1])
            if "playerhands" in msg[0]:
                print("playerhands received")
                plHands = decodeHands(msg[1])
                if plHands != []:
                    for i in range(len(self.players)):
                        self.players[i].hand = [plHands[2*i], plHands[2*i+1]]
                        print(self.players[i].hand)
                print('tablehands received', msg[2])
                self.status.allTableHand = decodeHands(msg[2])
                print('self.status.allTableHand:', self.status.allTableHand)
            elif 'myid' in msg[0]:
                print('My id is: %d' % int(msg[1]))
                self.whoAmI = int(msg[1])
            elif msg[0] == "newPlayer":
                print('%d joined the game' % pID)
                self.otherStrangers += 1
                print('Total Players: ', str(self.otherStrangers + 1))
                if self.otherStrangers == 3: self.startGame = True
            elif 'endGame' in msg[0]:
                self.status.getWinner(self.players)
                self.screen = 'gameOver'
            elif len(msg) == 4:
                amount = int(msg[2])
                if msg[1] == 'raise':
                    self.status.move('raise', pID, self.players, 
                        amount=amount, whoAmI=self.whoAmI)
                elif msg[1] == 'check/call':
                    self.status.move('check/call', pID, self.players, 
                        amount=0, whoAmI=self.whoAmI)
                else:
                    self.status.move('fold', pID, self.players, 
                        amount=0, whoAmI=self.whoAmI)
            
            serverMsg.task_done()


        if 2 not in self.status.betStatus:
            for i in range(len(self.status.betStatus)):
                if self.status.betStatus[i] != 0: self.status.betStatus[i]=2
            if len(self.status.tableHand) == 5 or\
            self.status.betStatus.count(0) == 3:
                self.status.nextRound(self, self.players, 
                    self.server, self.whoAmI)
                self.status.betStatus = [2] * len(self.players)
            else:
                print('Showing the next card(s)...')
                desired = max(len(self.status.tableHand) + 1, 3)
                self.status.tableHand = self.status.allTableHand[:desired]

        for player in self.players: 
            if player.money < 0: player.money = 0
        self.status.currentPlayer %= len(self.players)
        if self.status.gameOver == True: self.screen = 'gameOver'
        elif self.status.gameOver == False:
            self.timerDelay += 1
            for betID in self.status.betStatus:
                if self.players[betID].money == 0:
                    if self.players[betID].foldStatus == True:
                        self.status.betStatus[betID] = 0
                    else:
                        self.status.betStatus[betID] = 1
            if self.players[self.status.currentPlayer].foldStatus == True:
                self.status.currentPlayer += 1; return
            if PokerGame.isKeyPressed(self, pygame.K_UP) and\
                self.status.tempBet < self.players[0].money: 
                self.status.tempBet += 1
            if PokerGame.isKeyPressed(self, pygame.K_DOWN) and\
                self.status.tempBet >= self.status.minBet: 
                self.status.tempBet -= 1

    def redrawAll(self, screen):

        if self.screen == 'splash':
            drawTitle(self, screen)
            drawSplashButtons(self, screen)

        elif self.screen == 'game':
            drawBackground(self, screen)
            drawTableCards(self, screen)
            drawPlayerStatus(self, screen)
            drawPlayerCards(self, screen)
            drawGameButtons(self, screen)
            drawStatusBoard(self, screen)
            drawPokerChips(self, screen)
            drawTableChips(self, screen)

        elif self.screen == 'gameOver':
            drawTitle(self, screen)
            drawGameOver(self, screen)

        pygame.display.flip()

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, server=None, serverMsg=None, width=800, height=600,
        fps=60, title="Poker - Multiplayer Client"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.server = server
        self.serverMsg = serverMsg
        pygame.init()

    def run(self, server):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(self.title)

        self._keys = dict()

        self.init(server)
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            
        pygame.quit()

def main():
    game = PokerGame(server)
    game.run(server)

if __name__ == '__main__':
    main()