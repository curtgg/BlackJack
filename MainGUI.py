import sys, pygame
size = width, height = 1200, 750 #very odd size
pygame.init() #very important
green = 4,134,21 #defines game board colour
screen = pygame.display.set_mode(size)
title = "Blackjack" #title at top of window
screen.fill(green)  ##MUST BE CALLED TO HAVE GREEN DISPLAY ON SCREEN
pygame.display.set_caption(title, "Blackjack") #displays title top of window
Tfont = pygame.font.Font(None, 100) #get text font
Mfont = pygame.font.Font(None, 60) #get text font

gameName = Tfont.render("BLACKJACK",0,(0,0,0)) #titlescreen string
start = Mfont.render("Start",0,(0,0,0))#start string
ops = Mfont.render("Options",0,(0,0,0))#options string
quit = Mfont.render("Quit",0,(0,0,0))#quit string
def main():
    while 1: ###WHILE LOOP NECESSARY FOR SCREEN TO STAY OPEN
        for event in pygame.event.get():
            curs_pos = pygame.mouse.get_pos()
            cursX = curs_pos[0]
            cursY = curs_pos[1]
            click = pygame.mouse.get_pressed() #returns triple for some reason
            click = click[0] #only need first element
            print(click)
            if event.type == pygame.QUIT: sys.exit()

            #Quit button
            if click and (cursX >= 460 and cursX <= 560) and (cursY >=560 and cursY <=590):
                sys.exit()

        #TODO: Move elements to align nicer
        #TODO: BE sure to change arguments for when clicked on to new location(s)
        screen.blit(gameName,(400,100))#draw title
        screen.blit(start,(465,350))#draw start
        screen.blit(ops,(465,450))#draw options
        screen.blit(quit,(465,550))#draw quit




        pygame.display.flip() ##update display **very important**


main()
