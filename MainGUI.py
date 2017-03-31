import sys, pygame
size = width, height = 1200, 750 #very odd size
pygame.init() #very important
green = 4,134,21 #defines game board colour
screen = pygame.display.set_mode(size)
title = "Blackjack" #title at top of window
screen.fill(green)  ##MUST BE CALLED TO HAVE GREEN DISPLAY ON SCREEN
pygame.display.set_caption(title, "Blackjack") #displays title top of window
font = pygame.font.Font(None, 100) #get text font
gameName = font.render("BLACKJACK",0,(0,0,0)) #titlescreen string
start = font.render("Start",0,(0,0,0))#start string
ops = font.render("Options",0,(0,0,0))#options string
quit = font.render("Quit",0,(0,0,0))#quit string
while 1: ###WHILE LOOP NECESSARY FOR SCREEN TO STAY OPEN
    for event in pygame.event.get():
        curs_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #print(curs_pos)
        if event.type == pygame.QUIT: sys.exit()
        #if click[0] and ((curs_pos
        #start game

    screen.blit(gameName,(400,100))#draw title
    screen.blit(start,(465,350))#draw start
    screen.blit(ops,(465,450))#draw options
    screen.blit(quit,(465,550))#draw quit




    pygame.display.flip() ##update display **very important**
