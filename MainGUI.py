import sys, pygame
from time import sleep
from Cardpile import cardPile

size = width, height = 1200, 750 #very odd size
pygame.init() #very important
green = (4, 134, 21) #defines game board colour
white = (255, 255, 255)
black = (0, 0, 0) #used for buttons and for spades/clubs
red = (255, 0 ,0) #used for hearts/diamonds
tableRed = (190, 34, 34)#used for table
screen = pygame.display.set_mode(size)
title = "Blackjack" #title at top of window
pygame.display.set_caption(title, "Blackjack") #displays title top of window
Tfont = pygame.font.Font(None, 100) #get text font
Mfont = pygame.font.Font(None, 60) #get text font

cardWidth = 40
cardHeight = 60
cardPiles = []
cardSpots = 6
diamond = pygame.image.load("diamond.png")
club = pygame.image.load("club.png")
heart = pygame.image.load("heart.png")
spade = pygame.image.load("spade.png")

gameName = Tfont.render("BLACKJACK",0, black) #titlescreen string
start = Mfont.render("Start",0, black)#start string
ops = Mfont.render("Options",0, black)#options string
quit = Mfont.render("Quit",0, black)#quit string
back = Mfont.render("Back",0, black)#back string
hit = Mfont.render("Hit",0, black)#hit string
stand = Mfont.render("Stand",0, black)#stand string
double = Mfont.render("Double",0, black)#double string
split = Mfont.render("Split",0, black)#split string

Vfont = pygame.font.Font(None, 12)
value = "K"
colour = red
valueFont = Vfont.render(value, 0, colour)

###setting up booleans for different states of the game
titleScreen = True #starts as true because it starts here
startScreen = False
optionsScreen = False
initialDraw = False
c = cardPile(0)
while 1: ###WHILE LOOP NECESSARY FOR SCREEN TO STAY OPEN
    for event in pygame.event.get():
        curs_pos = pygame.mouse.get_pos()
        cursX = curs_pos[0]
        cursY = curs_pos[1]
        click = pygame.mouse.get_pressed() #returns triple for some reason
        click = click[0] #only need first element
        #print(click)
        if event.type == pygame.QUIT: sys.exit()

    #Title screen functionality
    if titleScreen:
        #TODO: Move elements to align nicer
        #TODO: BE sure to change arguments for when clicked on to new location(s)
        screen.fill(green)
        #i will fix the alignment of title and these later
        screen.blit(gameName,(400,100))#draw title
        screen.blit(start,(465,350))#draw start
        screen.blit(ops,(465,450))#draw options
        screen.blit(quit,(465,550))#draw quit

        #Quit button
        if click and (cursX >= 460 and cursX <= 560) and (cursY >=560 and cursY <=590):
            sys.exit()

        #Start button
        if click and (cursX >= 460 and cursX <= 570) and (cursY >=360 and cursY <=390):
            titleScreen = False
            startScreen = True
            initalDraw = True
            print("start game")

    #Start screen functionality, maybe we can change this to "gamescreen" later?
    if startScreen:
        #We only want to draw these things the first time we load the startScreen
        if initalDraw:
            cardx = 580
            cardy = 420
            dx = 40
            dy = 60
            screen.fill(green)
            pygame.draw.ellipse(screen, tableRed, [100, -500, 1000, 1000])#drawing of table
            pygame.draw.ellipse(screen, green, [375, -300, 450, 450])#can adjust this later, it's somewhat off
            pygame.draw.rect(screen, green, [0, 0, 1200, 50])
            #drawing buttons
            screen.blit(back,(1075,10))
            screen.blit(double,(260,625))
            screen.blit(hit,(485,625))
            screen.blit(stand,(635,625))
            screen.blit(split,(835,625))
            initalDraw = False
        #Back to title screen button
        if click and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
            titleScreen = True
            startScreen = False
            print("go to title")
        #Hit button
        if click and (cursX >= 475 and cursX <= 570) and (cursY >=615 and cursY <=665):
            #pygame.draw.rect(screen, white, [180, 170, dx, dy]) #p4
            #pygame.draw.rect(screen, white, [380, 350, dx, dy]) #p2

            #pygame.draw.rect(screen, white, [580, 420, dx, dy]) #p1 and drawing upwards
            #pygame.draw.rect(screen, white, [580, cardy, dx, dy])

            #pygame.draw.rect(screen, white, [780, 350, dx, dy]) #p3
            #pygame.draw.rect(screen, white, [980, 170, dx, dy]) #p5
            #pygame.draw.rect(screen, white, [580, 160, dx, dy]) #p0 aka the dealer

            #screen.blit(diamond, (cardx,cardy+dy-8))
            #screen.blit(diamond, (cardx+dx-8,cardy))
            #screen.blit(valueFont, (cardx+8,cardy+dy-8))
            #screen.blit(valueFont, (cardx+dx-8-8,cardy))

            cardy -= dy - 8

            # for i in range(cardSpots):
            c.drawCard(0,'C','K',screen)

            print("hit") #prints a million times, maybe need to implement delay so we dont deal a fuck ton of cards?
            sleep(0.1)

    pygame.display.flip() ##update display **very important**
