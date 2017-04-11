import sys, pygame
from time import sleep
from Cardpile import cardPile
from Game import initGame, startRound, initDeck

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
numDecks = 3
startBetMoney = 500 ###the starting money
#Load images
diamond = pygame.image.load("diamond.png")
club = pygame.image.load("club.png")
heart = pygame.image.load("heart.png")
spade = pygame.image.load("spade.png")

#define strings used and written in game
gameName = Tfont.render("BLACKJACK",0, black) #titlescreen string
start = Mfont.render("Start",0, black)#start string
ops = Mfont.render("Options",0, black)#options string
optionsTitle = Tfont.render("Options", 0, black)
quit = Mfont.render("Quit",0, black)#quit string
back = Mfont.render("Back",0, black)#back string
hit = Mfont.render("Hit",0, black)#hit string
stand = Mfont.render("Stand",0, black)#stand string
double = Mfont.render("Double",0, black)#double string
split = Mfont.render("Split",0, black)#split string
betString = Mfont.render("Bet",0,black)
numHumans = Mfont.render("Number of Humans",0, black)
numComputers = Mfont.render("Number of Computers",0, black)
numStartDecks = Mfont.render("Number of Starting Decks",0, black)
startBetM= Mfont.render("Starting Bet Money",0, black)
showCountOpt = Mfont.render("Show Card Count",0, black)
blackYes = Mfont.render("Yes /",0, black) #used when card count off
redYes = Mfont.render("Yes",0, tableRed) #used when card count off
blackNo = Mfont.render("/ No",0, black) #used when card count on
redNo = Mfont.render("No",0, tableRed) #used when card count on
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
showCount = False


def getInput():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            return event.key
        if event.type == pygame.QUIT: sys.exit()

#draws options screen
def drawOptionsScreen():
    screen.fill(green)
    #drawing the boxes for the first four options
    xDraw = 955
    yDraw = 140
    for i in range(3):
        pygame.draw.polygon(screen, tableRed, ((xDraw, yDraw+16), (xDraw+20, yDraw), (xDraw+40, yDraw +16)))
        pygame.draw.rect(screen, white, (xDraw, yDraw+20, 40, 40))
        pygame.draw.polygon(screen, tableRed, ((xDraw, yDraw+64), (xDraw+20, yDraw+80), (xDraw+40, yDraw +64)))
        yDraw += 100

    pygame.draw.polygon(screen, tableRed, ((940, yDraw+16), (940+38, yDraw), (938+76, yDraw +16)))
    pygame.draw.rect(screen, white, (938, 460, 76, 40))
    pygame.draw.polygon(screen, tableRed, ((940, yDraw+64), (940+38, yDraw+76), (938+76, yDraw +64)))

    screen.blit(optionsTitle,(460,20))#draw title
    screen.blit(numHumans,(200,160))
    screen.blit(numComputers,(200,260))
    screen.blit(numStartDecks,(200,360))
    screen.blit(startBetM,(200,460))
    screen.blit(showCountOpt,(200,560))
    screen.blit(back,(548,690))

    ###drawing the changing parts of the menu
    #indicating whether or not count is on
    if showCount:
        screen.blit(redYes,(900,560))
        screen.blit(blackNo,(980,560))
    else:
        screen.blit(blackYes,(900,560))
        screen.blit(redNo,(1000,560))

    #drawing the changing numbers
    humansString = Mfont.render((str(playCount)),0,black)
    cmptString = Mfont.render((str(botCount)),0,black)
    decksString = Mfont.render((str(numDecks)),0,black)
    betMoneyString = Mfont.render((str(startBetMoney)),0,black)

    screen.blit(humansString,(965,160))
    screen.blit(cmptString,(965,260))
    screen.blit(decksString,(965,360))
    screen.blit(betMoneyString,(940,460))
    pygame.display.flip() ##update display **very important**


    #pygame.draw.line(screen, red, (600,0), (600,750)) #red line down center


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
    click = 0
    clickN = pygame.mouse.get_pressed()[0] #get left click
    if clickN == 1 and click == 1:
        pass
    else:
        click = clickN
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

        #Options button
        if click and (cursX >= 517 and cursX <= 695) and (cursY >=440 and cursY <=480):
            titleScreen = False
            optionsScreen = True

    #Start screen functionality, maybe we can change this to "gamescreen" later?
    if startScreen:
        drawGameScreen()
        if startGame:
            #players, bots, decknums
            (deck,dealer) = initGame(playCount,botCount,numDecks,screen,showCount,startBetMoney)
            startGame = False
            cont = True
        #start gets set to false when player selects back
        while cont:
            cont = startRound(deck, dealer)
            #reshuffle if smaller than 25 cards remaining
            if (deck.deckSize()) < 25:
                deck.burnCards(deck.deckSize)
                deck = initDeck(deck)

            drawGameScreen()

        if not cont:
            titleScreen = True
            startScreen = False

    #Options screen functionality
    if optionsScreen:
        while optionsScreen:

            click = pygame.mouse.get_pressed()[0] #get left click
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                click = pygame.mouse.get_pressed()[0] #get left click
                (cursX, cursY) = pygame.mouse.get_pos()

            drawOptionsScreen()

            #Button for showing count
            if click and (cursX >= 890 and cursX <= 1050) and (cursY >=560 and cursY <=600):
                if showCount:
                    showCount = False
                else:
                    showCount = True

                print(showCount)    
                sleep(0.2)


            #Buttons for changing deck number
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=340 and cursY <=356) and (numDecks < 5):
                numDecks += 1
                sleep(0.2)
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=404 and cursY <=420) and (numDecks > 1):
                numDecks -= 1
                sleep(0.2)

            #Button for changing number of bots
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=240 and cursY <=256) and ((botCount + playCount) < 5):
                botCount += 1
                sleep(0.2)
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=304 and cursY <=320) and ((botCount) > 0):
                botCount -= 1
                sleep(0.2)

            #Button for changing number of humans
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=140 and cursY <=156) and ((botCount + playCount) < 5):
                playCount += 1
                sleep(0.2)
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=204 and cursY <=220) and ((playCount) > 1):
                playCount -= 1
                sleep(0.2)

            #Button for changing starting bet money
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=440 and cursY <=456) and (startBetMoney < 900):
                startBetMoney += 100
                sleep(0.2)
            elif click and (cursX >= 950 and cursX <= 1000) and (cursY >=504 and cursY <=520) and (startBetMoney > 100):
                startBetMoney -= 100
                sleep(0.2)

            #Button for back to menu
            elif click and (cursX >= 545 and cursX <= 650) and (cursY >=690 and cursY <=730):
                optionsScreen = False
                titleScreen = True
                initialDraw = True

    pygame.display.flip() ##update display **very important**
