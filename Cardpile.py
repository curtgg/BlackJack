import sys, pygame
import time

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0) #used for buttons and for spades/clubs
red = (255, 0 ,0) #used for hearts/diamonds
green = (4, 134, 21) #defines game board colour
tableRed = (190, 34, 34)#used for table

diamond = pygame.image.load("Icons/diamond.png")
club = pygame.image.load("Icons/club.png")
heart = pygame.image.load("Icons/heart.png")
spade = pygame.image.load("Icons/spade.png")
Vfont = pygame.font.Font(None, 12) #get text font
Mfont = pygame.font.Font(None, 36) #middle card font
Pfont = pygame.font.Font(None,25)
cardWidth = 40
cardHeight = 60


class cardPile:


    def __init__(self, position):
        self.position = position
        self.numCards = 0
        self.splitCards = 0

    def drawCard(self, player, screen):
        '''
        Draws cards that are dealt including splits
        Args:
            player - Player object
            screen - The game screen we draw onto
        '''
        #the player's cards are a tuple, with suit being 0 and value being 1
        if player.split:
            suit = player.hand2[-1][0]
            value = player.hand2[-1][1]
        else:
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
        if not player.split:
            if self.position == 0 and self.numCards > 0:
                x += (0 + (self.numCards*16))
            #if player shift up for successive cards
            elif self.position != 0 and self.numCards > 0:
                 y -= (0 + ((self.numCards)*8)) #need to adjust where the card is drawn
                                                       #based on how many cards were drawn before it
        else:
            if self.position == 0 and self.numCards > 0:
                x += (0 + (self.splitCards*16))
            #if player shift up for successive cards
            elif self.position != 0 and self.numCards > 0:
                 y -= (0 + ((self.splitCards)*8)) #need to adjust where the card is drawn
                                                       #based on how many cards were drawn before it



        pygame.draw.rect(screen, white, [x, y, cardWidth, cardHeight])
        screen.blit(suit,(x, y+cardHeight-8))
        screen.blit(suit,(x+cardWidth-8, y))
        screen.blit(valueFont, (x+8,y+cardHeight-8))
        screen.blit(valueFont, (x+cardWidth-8-8,y))

        letterValues = {'A','J','K','Q'}
        if value in letterValues:
            screen.blit(middleFont, (x+12, y+18))
        elif value == '10':
            screen.blit(middleFont, (x+7, y+18))
        else:
            screen.blit(middleFont, (x+14, y+18))

        if player.split:
            self.splitCards += 1
        else:
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

    def splitCard(self, player,screen):
        '''
        Call after you preform split function from player class
        removes old cards and places the 2 split cards independently
            Args:
            Self - cardpile object
            player - player object
            screen - display
        '''
        self.splitCards = 0
        self.numCards = 0
        #below, x1,y1 is card of main hand
        # x2,y2 is pos of second hand card
        if self.position == 0:
            return
        elif self.position == 1:
            x1 = 580
            y1 = 420
            x2 = 630
            y2 = 420
        elif self.position == 2:
            x1 = 380
            y1 = 350
            x2 = 430
            y2 = 350
        elif self.position == 3:
            x1 = 780
            y1 = 350
            x2 = 830
            y2 = 350
        elif self.position == 4:
            x1 = 180
            y1 = 170
            x2 = 230
            y2 = 170
        elif self.position == 5:
            x2 = 980
            y2 = 170
            x1 = 930
            y1 = 170
        pygame.draw.rect(screen,tableRed,[x1,y1-10,cardWidth*2+15,cardHeight+10])
        #cover old cards

        #get values
        card1 = player.hand[0]
        card2 = player.hand2[0]
        suit1 = card1[0]
        suit2 = card2[0]
        value1 = card1[1]
        value2 = card2[1]

        #get respective suits
        if suit1 == ('D'):
            colour1 = red
            suit1 = diamond
        elif suit1 == ('S'):
            colour1 = black
            suit1 = spade
        elif suit1 == ('C'):
            colour1 = black
            suit1 = club
        elif suit1 == ('H'):
            colour1 = red
            suit1 = heart
        valueFont1 = Vfont.render(value1, 0, colour1)
        middleFont1 = Mfont.render(value1, 0, colour1)

        if suit2 == ('D'):
            colour2 = red
            suit2 = diamond
        elif suit2 == ('S'):
            colour2 = black
            suit2 = spade
        elif suit2 == ('C'):
            colour2 = black
            suit2 = club
        elif suit2 == ('H'):
            colour2 = red
            suit2 = heart

        #get respective colours
        valueFont2 = Vfont.render(value2, 0, colour2)
        middleFont2 = Mfont.render(value2, 0, colour2)

        #draw both cards
        pygame.draw.rect(screen, white, [x1, y1, cardWidth, cardHeight])
        screen.blit(suit1,(x1, y1+cardHeight-8))
        screen.blit(suit1,(x1+cardWidth-8, y1))
        screen.blit(valueFont1, (x1+8,y1+cardHeight-8))
        screen.blit(valueFont1, (x1+cardWidth-8-8,y1))

        pygame.draw.rect(screen, white, [x2, y2, cardWidth, cardHeight])
        screen.blit(suit2,(x2, y2+cardHeight-8))
        screen.blit(suit2,(x2+cardWidth-8, y2))
        screen.blit(valueFont2, (x2+8,y2+cardHeight-8))
        screen.blit(valueFont2, (x2+cardWidth-8-8,y2))


        letterValues = {'A','J','K','Q'}
        #draw card values
        if value1 in letterValues:
            screen.blit(middleFont1, (x1+12, y1+18))
        elif value1 == '10':
            screen.blit(middleFont1, (x1+7, y1+18))
        else:
            screen.blit(middleFont1, (x1+14, y1+18))

        if value2 in letterValues:
            screen.blit(middleFont2, (x2+12, y2+18))
        elif value2 == '10':
            screen.blit(middleFont2, (x2+7, y2+18))
        else:
            screen.blit(middleFont2, (x2+14, y2+18))

        self.splitCards = 1
        self.numCards = 1
