import sys, pygame
size = width, height = 1200, 750 #very odd size
pygame.init() #very important
green = 4,134,21 #defines game board colour
screen = pygame.display.set_mode(size)
title = "Blackjack" #title at top of window
screen.fill(green)  ##MUST BE CALLED TO HAVE GREEN DISPLAY ON SCREEN
pygame.display.set_caption(title, "Blackjack") #displays title top of window
pygame.display.flip() ##IF FLIP NOT CALLED, DISPLAYS OFF SCREEN
while 1: ###WHILE LOOP NECESSARY FOR SCREEN TO STAY OPEN
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
