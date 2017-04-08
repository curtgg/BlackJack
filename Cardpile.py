import sys, pygame

###not sure how much of this block is necessary, i just threw a lot of shit in
#while i was trying to get this to work

pygame.init()
numCards = 0
white = (255, 255, 255)
black = (0, 0, 0) #used for buttons and for spades/clubs
red = (255, 0 ,0) #used for hearts/diamonds
diamond = pygame.image.load("diamond.png")
club = pygame.image.load("club.png")
heart = pygame.image.load("heart.png")
spade = pygame.image.load("spade.png")
Vfont = pygame.font.Font(None, 12) #get text font
cardWidth = 8
cardHeight = 8


class cardPile:


    def __init__(self, position):
        self.position = position
        self.numCards = 1

    ###when giving inputs to this, i think we will have to split the tuples that are made
      #when the cards are dealt for suit and value
    def drawCard(self, position, suit, value, screen):
        ###this is the lazy code i talked about, not sure of the best way to do lines 26-56
        if self.position == 0:
            x = 580
            y = 160
        if self.position == 1:
            x = 580
            y = 420
        if self.position == 2:
            x = 380
            y = 350
        if self.position == 3:
            x = 780
            y = 350
        if self.position == 4:
            x = 180
            y = 170
        if self.position == 5:
            x = 980
            y = 170

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

        y -= (cardHeight + ((self.numCards)*8)) #need to adjust where the card is drawn
                                               #based on how many cards were drawn before it

        
        valueFont = Vfont.render(value, 0, colour) #not sure if this is needed,
                                                        #put it in while testing

        pygame.draw.rect(screen, white, [x, y, cardWidth, cardHeight])
        screen.blit(suit,(x, y+cardHeight-8))
        screen.blit(suit,(x+cardWidth-8, cardHeight))
        screen.blit(valueFont, (x+8,y+cardHeight-8))
        screen.blit(valueFont, (x+cardWidth-8-8,y))

        self.numCards += 1


    def clearCard():
        #essentially just redrawing the table
        pass

    def splitCard(self, position, suit, value):
        #redraw table at position, draw first card again and then draw second card beside it
        pass
