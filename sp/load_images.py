import pygame, os

def loadBGBoard(self, screen, xOffset, yOffset):
    filepath = os.path.join('sp', 'Resources', 'status-board.jpg')
    image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
        (int(self.width) - 2 * xOffset, int(self.height) - 2 * yOffset))
    return image

def getBoardImage(width, height):
    filepath = os.path.join('sp', 'Resources', 'poker-table.jpg')
    image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
        (width, height))
    return image

def getSplashBG(width, height):
    filepath = os.path.join('sp', 'Resources', 'splash-bg.jpg')
    image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
        (width, height))
    return image

def getStatusBoardImage(self, scale):
    filepath = os.path.join('sp', 'Resources', 'status-board.jpg')
    image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
        (int(self.width/scale), int(self.height/scale)))
    return image

def getCardImages(scale):
    width = 2*scale
    height = 3*scale

    def getSuit(filepath):
        if filepath == 'back.png': 
            return 'back'
        path = filepath.split('_')
        other = ['ace', 'jack', 'king', 'queen']
        if str(path[0]).isdigit() or path[0] in other:
            suit = path[-1].split('.')
            suit = suit[0]
            return suit

    def getValue(filepath):
        if filepath == 'back.png': 
            return 'back'
        path = filepath.split('_')
        other = ['ace', 'jack', 'king', 'queen']
        if str(path[0]).isdigit() or path[0] in other:
            return path[0]

    result = {'clubs': {}, 'diamonds': {}, 'hearts': {}, 'spades': {}, 
        'back': {}}
    cardList = os.listdir(os.path.join('sp', 'Resources', 'playing_cards'))
    for cardPath in cardList:
        if cardPath.count('_') == 2 or cardPath == 'back.png':
            cardDir = os.path.join('sp', 'Resources', 'playing_cards', cardPath)
            cardImage = pygame.transform.scale(pygame.image.load(cardDir).\
                convert_alpha(), (width, height))
            suit = getSuit(cardPath)
            value = getValue(cardPath)
            result[suit][value] = cardImage
    return result

def getButtonImages():
    buttons = {}
    def getButton(name):
        folder = os.path.join('sp', 'Resources', 'buttons')
        filepath = '/button_' + name + '.png'
        image = pygame.image.load(folder + filepath)
        return image
    for file in ['fold', 'raise', 'check-call']:
        buttons[file] = getButton(file)
    return buttons

def getTitleButtons():
    buttons = {}
    def getButton(name):
        folder = os.path.join('sp', 'Resources', 'title')
        filepath = '/button_' + name + '.png'
        image = pygame.image.load(folder + filepath)
        return image
    for file in ['CA314-poker', 'start-game']:
        buttons[file] = getButton(file)
    return buttons

def getHomeButton():
    def getButton(name):
        folder = os.path.join('sp', 'Resources', 'buttons')
        filepath = '/button_' + name + '.png'
        image = pygame.image.load(folder + filepath)
        return image
    button = getButton('home')
    return button

def getEndGameButton():
    def getButton(name):
        folder = os.path.join('sp', 'Resources', 'buttons')
        filepath = '/button_' + name + '.png'
        image = pygame.image.load(folder + filepath)
        return image
    button = getButton('end-game')
    return button
