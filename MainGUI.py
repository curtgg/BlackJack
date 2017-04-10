import sys, pygame
from time import sleep
from Cardpile import cardPile
from Game import initGame, startRound

size = width, height = 1200, 750 #very odd size
pygame.init() #very important
green = (4, 134, 21) #defines game board colour
white = (255, 255, 255)
black = (0, 0, 0) #used for buttons and for spades/clubs
red = (255, 0 ,0) #used for hearts/diamonds
blue = (59, 57, 183) #used for chips
tableRed = (190, 34, 34)#used for table
screen = pygame.display.set_mode(size)
title = "Blackjack" #title at top of window
pygame.display.set_caption(title, "Blackjack") #displays title top of window
Tfont = pygame.font.Font(None, 100) #get text font
Mfont = pygame.font.Font(None, 60) #get text font\
Nfont = pygame.font.Font(None, 20) #text on chips

playCount = 1 #number of players
botCount = 0 #number of bots

cardWidth = 40
cardHeight = 60
cardPiles = []
cardSpots = 6
#Load images
diamond = pygame.image.load("diamond.png")
club = pygame.image.load("club.png")
heart = pygame.image.load("heart.png")
spade = pygame.image.load("spade.png")

#define strings used and written in game
gameName = Tfont.render("BLACKJACK",0, black) #titlescreen string
start = Mfont.render("Start",0, black)#start string
ops = Mfont.render("Options",0, black)#options string
quit = Mfont.render("Quit",0, black)#quit string
back = Mfont.render("Back",0, black)#back string
hit = Mfont.render("Hit",0, black)#hit string
stand = Mfont.render("Stand",0, black)#stand string
double = Mfont.render("Double",0, black)#double string
split = Mfont.render("Split",0, black)#split string
betString = Mfont.render("Bet",0,black)
ten = Nfont.render("10",0,black)
five = Nfont.render("5",0,black)
one = Nfont.render("1",0,black)
Vfont = pygame.font.Font(None, 12)

###setting up booleans for different states of the game
titleScreen = True #starts as true because it starts here
startScreen = False
optionsScreen = False
startGame = False
cont = False


def getInput():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            return event.key
        if event.type == pygame.QUIT: sys.exit()

#draws options screen
def drawOptions():
    pass

#draws title screen
def drawTitleScreen():
    #TODO: Move elements to align nicer
    #TODO: BE sure to change arguments for when clicked on to new location(s)
    screen.fill(green)
    #i will fix the alignment of title and these later
    screen.blit(gameName,(400,100))#draw title
    screen.blit(start,(465,350))#draw start
    screen.blit(ops,(465,450))#draw options
    screen.blit(quit,(465,550))#draw quit
    pygame.display.flip() ##update display **very important**
    pass

#draws and updates game screen
def drawGameScreen():
    cardx = 580
    cardy = 420
    dx = 40
    dy = 60
    screen.fill(green)
    pygame.draw.ellipse(screen, tableRed, [100, -500, 1000, 1000])#drawing of table
    pygame.draw.ellipse(screen, green, [375, -300, 450, 450])#can adjust this later, it's somewhat off
    pygame.draw.rect(screen, green, [0, 0, 1200, 50])

    #NOTE:ten chips in range X:[1005,1065] Y:[495,555]
    pygame.draw.circle(screen,black,(1035,525),30) #draw ten chip, larger circ
    pygame.draw.circle(screen,white,(1035,525),20) #draw ten chip
    screen.blit(ten,(1028,520)) #draw 10 on chip
    #NOTE:five chips in range X:[1080,1140] Y:[495,555]
    pygame.draw.circle(screen,blue,(1110,525),30) #draw five chip, larger circ
    pygame.draw.circle(screen,white,(1110,525),20) #draw five chip
    screen.blit(five,(1105,520)) #draw 5 on chip
    #NOTE:one chips in range X:[1042,1102] Y:[555,615]
    pygame.draw.circle(screen,red,(1072,585),30) #draw one chip, larger circ
    pygame.draw.circle(screen,white,(1072,585),20) #draw one chip
    screen.blit(one,(1069,580)) #draw 1 on chip

    #drawing buttons
    screen.blit(back,(1075,10))
    screen.blit(double,(260,625))
    screen.blit(hit,(485,625))
    screen.blit(stand,(635,625))
    screen.blit(split,(835,625))
    screen.blit(betString,(1035,455))

    #TODO: DRAW PLAYER MONEY AND BET

    pygame.display.flip() ##update display **very important**





while 1: ###WHILE LOOP NECESSARY FOR SCREEN TO STAY OPEN
    curs_pos = pygame.mouse.get_pos()
    (cursX, cursY) = (curs_pos)
    click = pygame.mouse.get_pressed()[0] #get left click
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #Title screen functionality
    if titleScreen:
        drawTitleScreen()
        #Quit button
        if click and (cursX >= 460 and cursX <= 560) and (cursY >=560 and cursY <=590):
            sys.exit()

        #Start button
        if click and (cursX >= 460 and cursX <= 570) and (cursY >=360 and cursY <=390):
            titleScreen = False
            startScreen = True
            startGame = True
            print("start game")

    #Start screen functionality, maybe we can change this to "gamescreen" later?
    if startScreen:
        drawGameScreen()
        if startGame:
            #players, bots, decknums
            (deck,dealer) = initGame(playCount,botCount,3,screen)
            startGame = False
            cont = True
        #start gets set to false when player selects back
        while cont:
            drawGameScreen()
            cont = startRound(deck, dealer)

        if not cont:
            titleScreen = True
            startScreen = False

    pygame.display.flip() ##update display **very important**
