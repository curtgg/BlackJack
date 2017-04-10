import sys, pygame
import time
###not sure how much of this block is necessary, i just threw a lot of shit in
#while i was trying to get this to work

pygame.init()
# numCards = 0
white = (255, 255, 255)
black = (0, 0, 0) #used for buttons and for spades/clubs
red = (255, 0 ,0) #used for hearts/diamonds
green = (4, 134, 21) #defines game board colour

diamond = pygame.image.load("diamond.png")
club = pygame.image.load("club.png")
heart = pygame.image.load("heart.png")
spade = pygame.image.load("spade.png")
Vfont = pygame.font.Font(None, 12) #get text font
Mfont = pygame.font.Font(None, 36) #middle card font
Pfont = pygame.font.Font(None,25)
cardWidth = 40
cardHeight = 60


class cardPile:


    def __init__(self, position):
        self.position = position
        self.numCards = 0

    ###when giving inputs to this, i think we will have to split the tuples that are made
      #when the cards are dealt for suit and value
    def drawCard(self, player, screen):
        suit = player.hand[-1][0]
        value = player.hand[-1][1]

        if suit == ('D'):
            colour = red
            suit = diamond
        elif suit == ('S'):
            colour = black
            suit = spade
        elif suit == ('C'):
            colour = black
            suit = club
        elif suit == ('H'):
            colour = red
            suit = heart
        valueFont = Vfont.render(value, 0, colour)
        middleFont = Mfont.render(value, 0, colour)

        #test
        if self.position == 0:
            x = 580
            y = 160
        elif self.position == 1:
            x = 580
            y = 420
            if player.split:
                x = 630
                y = 420
        elif self.position == 2:
            x = 380
            y = 350
            if player.split:
                x = 430
                y = 350
        elif self.position == 3:
            x = 780
            y = 350

            if player.split:
                x = 830
                y = 350
        elif self.position == 4:
            x = 180
            y = 170

            if player.split:
                x = 230
                y = 170
        elif self.position == 5:
            x = 980
            y = 170
            if player.split:
                x = 930
                y = 170


        #if dealer move cards right for successive cards
        if self.position == 0 and self.numCards > 0:
            x += (0 + (self.numCards*16))
        #if player shift up for successive cards
        elif self.position != 0 and self.numCards > 0:
             y -= (0 + ((self.numCards)*8)) #need to adjust where the card is drawn
                                                   #based on how many cards were drawn before it



        pygame.draw.rect(screen, white, [x, y, cardWidth, cardHeight])
        screen.blit(suit,(x, y+cardHeight-8))
        screen.blit(suit,(x+cardWidth-8, y))
        screen.blit(valueFont, (x+8,y+cardHeight-8))
        screen.blit(valueFont, (x+cardWidth-8-8,y))

        ###for some reason if the numbers were centered, the letters wouldnt be.
        #  so i had to create different cases
        letterValues = {'A','J','K','Q'}
        if value in letterValues:
            screen.blit(middleFont, (x+12, y+18))
        elif value == '10':
            screen.blit(middleFont, (x+7, y+18))
        else:
            screen.blit(middleFont, (x+14, y+18))

        self.numCards += 1


    def drawStats(self,money,bet,cSum,cSum2,split,screen):
        '''
        Function used to update the players stats such as their bet and cash stack.

        Args:
            self - Cardpile object corresponding to the player we wish to update stats on
            money - Players money
            bet - players current bet
            screen - current display
        '''
        #this shouldnt happen
        if self.position == 0:
            return
        elif self.position == 1:
            x = 580
            y = 505
        elif self.position == 2:
            x = 280
            y = 450
        elif self.position == 3:
            x = 845
            y = 440
        elif self.position == 4:
            x = 60
            y = 250
        elif self.position == 5:
            x = 1055
            y = 250

        pygame.draw.rect(screen,green,[x,y,90,70]) #cover old stats
        money = Pfont.render("Cash: " + str(money),0,black)
        bet = Pfont.render("Bet: " + str(bet),0,black)
        if split:
            cardSum = Pfont.render("Sum: " + str(int(cSum)) + ", " + str(int(cSum2)),0,black)
        else:
            cardSum = Pfont.render("Sum: " + str(cSum),0,black)
        screen.blit(money,(x,y))
        screen.blit(bet,(x,y+20))
        screen.blit(cardSum,(x,y+40))


    def clearCard(self):
        self.numCards = 0

    def splitCard(self, position, suit, value):
        #redraw table at position, draw first card again and then draw second card beside it
        pass
