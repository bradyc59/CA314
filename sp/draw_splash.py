import pygame
from load_images import *

def drawTitle(self, screen):
    background = getSplashBG(self.width, self.height)
    screen.blit(background, (0,0))

def drawSplashButtons(self, screen):
    buttons = getTitleButtons()
    self.startButtons = {}
    
    centerSpacing = self.height // (len(buttons)+1); i = 0
    for buttonName in ['CA314-poker', 'start-game']:
        button = buttons[buttonName]
        buttonWidth = pygame.Surface.get_width(button)
        buttonHeight = pygame.Surface.get_height(button)
        cx, cy = self.width//2, centerSpacing * (i+1)
        topLX, topLY = cx - buttonWidth//2, cy - buttonHeight//2
        screen.blit(button, (topLX, topLY))
        i += 1
        self.startButtons[buttonName] = (topLX, topLX + buttonWidth, topLY, 
            topLY + buttonHeight)