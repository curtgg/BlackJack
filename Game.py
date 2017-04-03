from Deck import Deck
from Player import Player
import pygame

playCount = 2 #number of players
botCount = 0 #number of bots
deckNum = 1 #number of decks sepecified
deckCount = 0 #deck count, for counting cards
playList = []
dealerHand = []
pygame.init()
size = width, height = 1200, 750 #very odd size
screen = pygame.display.set_mode(size)

def getDealerTurn(deck):
    '''
    Computes the dealer hand.
    TODO: add more
    Args:
        deck - Deck object, pre initialized
    '''
    def clearDealerHand():
        '''
        clears dealer hand, used after new game
        '''
        dealerHand = []


    def getSum():
        '''
`       Gets sum of dealers hand
        '''
        letters = {'A','J','K','Q'}
        cSum = 0
        for i in range(len(dealerHand)):
            cardval = dealerHand[i][1]
            if cardval in letters:
                if cardval == 'A':
                    cSum += 11
                else:
                    cSum += 10
            else:
                cardval = int(cardval)
                cSum += cardval
        print("Dealer Sum: {}".format(cSum))
        return cSum
    #only if <2, as in start of round
    if len(dealerHand) < 2:
        dealerHand.append(deck.draw())
        dealerHand.append(deck.draw())
        print("Dealer Hand: {}".format(dealerHand))
        return (dealerHand[0][0],getSum())
    else:
        #NOTE:wont hit on 17, may need to change dependent
        #NOTE:on what we deside to do
        if getSum() < 17:
            dealerHand.append(deck.draw())
        else:
            #TODO: maybe do something if hes not hitting?
            pass

    #NOTE:Return dealers first card and sum
    return (dealerHand[0][1],getSum())



def getPlayerTurn(player,deck):
    '''
    Gets the players turn
    Args:
        player - Player object
    '''
    turnOver = False
    def getSum():
        '''
`       Gets sum of dealers hand
        '''
        letters = {'A','J','K','Q'}
        cSum = 0
        for i in range(len(player.hand)):
            cardval = player.hand[i][1]
            if cardval in letters:
                if cardval == 'A':
                    cSum += 11
                else:
                    cSum += 10
            else:
                cardval = int(cardval)
                cSum += cardval
        print("Player Sum: {}".format(cSum))
        return cSum

    def getBet():
        while True:
            pass

    def getAction():
        '''
        Get user action, i.e Hit, split etc
        '''
        while True:
            #TODO: MAKE GET INPUT FUNCTION
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        print("yay")


    if len(player.hand) < 2:
        player.addCard(deck.draw())
        player.addCard(deck.draw())
        print("Player Hand: {}".format(player.hand))
        getSum()
    while True:
        #TODO: compute bet
        #getBet()
        getAction()
        if turnOver == True:
            break

def initDeck(deck):
    deck.newDeck(deckNum)
    deck.shuffle()
    return deck

def startGame():
    #Add players
    #print(deck._array)
    for i in range(playCount):
        player = Player()
        playList.append(player)

    deck = Deck() #init deck
    deck = initDeck(deck)

    #print(playList)
    while True:
        result = getDealerTurn(deck)
        #print("Dealer First card and Sum: {}".format(result))
        for i in range(playCount):
            player = playList[i]
            getPlayerTurn(player,deck)



startGame()
