from Deck import Deck
from Player import Player, Dealer
import pygame
import time
from Cardpile import cardPile
deckNum = 5 #number of decks sepecified
playList = []
screenL = []
pCards = []
black = (0,0,0)
green = (4, 134, 21) #defines game board colour

Mfont = pygame.font.Font(None, 40) #get text font
sumD = Mfont.render("Dealers Sum:",0, black)#sum string
#TODO:draw split handling
def updateStats(player):
    #TODO:split handling
    cPile = pCards[player.num+1]
    cPile.drawStats(player.money,player.bet,player.cardSum,player.cardSum2,player.splitV,screenL[0])
    pygame.display.flip() ##update display **very important**



def getBet(player,deck):
    #no money to play
    if player.money < 5:
        return
    else:
        if not player.bot:
            print("Whats your bet? Up: +5, Down: -5")
            while True:
                (cursX,cursY,clickL,clickR) = getInput()
                #TODO: sometimes if you hold mouse or something this goes crazy
                #otherwise this works fine
                if (clickL or clickR) and (cursX >= 1005 and cursX <= 1065) and (cursY >=495 and cursY <=555):
                    if clickL and ((player.money-player.bet) >= 10):
                        player.bet += 10
                        time.sleep(0.5)
                    elif clickR and ((player.bet) > 10):
                        player.bet -= 10
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #five chip
                elif (clickL or clickR) and (cursX >= 1080 and cursX <= 1140) and (cursY >=495 and cursY <=555):
                    if clickL and ((player.money-player.bet) >= 5):
                        player.bet += 5
                        time.sleep(0.5)
                    elif clickR and ((player.bet) > 5):
                        player.bet -= 5
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #one chip
                elif (clickL or clickR) and (cursX >= 1042 and cursX <= 1102) and (cursY >=555 and cursY <=615):
                    if clickL and ((player.money-player.bet) >= 1):
                        player.bet += 1
                        time.sleep(0.5)
                    elif clickR and ((player.bet) > 1):
                        player.bet -= 1
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #Back to main menu
                if clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True
                elif clickL and (cursX >= 1038 and cursX <= 1102) and (cursY >= 461 and cursY <=486):
                    return False
                updateStats(player)
        else:
            #NOTE: IF bot compute the bet
            time.sleep(1)
            player.computeBet(deck)
            updateStats(player)
            print("Player Bet:{} and count: {}".format(player.bet,deck.count))

def drawDealer(dealer,card):
    pygame.draw.rect(screenL[0],green,[670,80,40,40])
    time.sleep(0.2)
    D = Mfont.render(str(dealer.cardSum),0, black)#sum string
    cPile = pCards[0]
    cPile.drawCard(dealer,screenL[0])
    screenL[0].blit(sumD,(490,90))
    screenL[0].blit(D,(680,90))
    pygame.display.flip() ##update display **very important**

def drawCards(player,card):
    cPile = pCards[player.num+1]
    cPile.drawCard(player,screenL[0])
    pygame.display.flip() ##update display **very important**


def getInput():
    events = pygame.event.get()
    curs_pos = pygame.mouse.get_pos()
    (cursX, cursY) = (curs_pos)
    (clickL,mid,clickR) = pygame.mouse.get_pressed() #get left click
    for event in events:
        if event.type == pygame.QUIT: sys.exit() #exits game
    #Returns mouse XY and if click
    return (cursX,cursY,clickL,clickR)

def getDealerTurn(deck,dealer):
    '''
    Computes the dealer hand.
    TODO: add more
    Args:
        deck - Deck object, pre initialized
    '''
    # if greater than or equal to 2, we know its hand from
    #prev round
    if dealer.done:
        dealer.clearHand()
        pCards[0].clearCard()

    #only if <1, as in start of round
    if len(dealer.hand) < 1:
        dealer.draw(deck)
        drawDealer(dealer,dealer.hand[-1])
        print("Dealer Hand: {}".format(dealer.hand))
        return (dealer.hand,dealer.cardSum)

    #NOTE:wont hit on 17, may need to change dependent
    #NOTE:on what we deside to do
    print("Dealer Hand: {} and Sum: {}".format(dealer.hand,dealer.cardSum))
    while dealer.cardSum < 17 or (dealer.cardSum == 17 and dealer.ace):
        dealer.draw(deck)
        drawDealer(dealer,dealer.hand[-1])
        time.sleep(1)
        print("Dealer Hand: {} and Sum: {}".format(dealer.hand,dealer.cardSum))
    time.sleep(4)
    return (dealer.hand,dealer.cardSum)



def getPlayerTurn(player,deck,dealer):
    '''
    Gets the players turn
    Args:
        player - Player object
    '''
    turnOver = False
    def doSplit(deck,player):
        print("Make your move for hand 2, hit-1, stand-2, double-3, split-4?")
        #NOTE:Absolutely zero support for more than 1 splits
        if player.bot:
            player.Hit(deck)
            drawCards(player,player.hand[-1])
            updateStats(player)
            while True:
                time.sleep(1)
                turn = player.computeTurn(deck,dealer.hand)
                #Hit
                if turn == 'H' or turn == 'X':
                    #force hit on a split, only 1 split allowed
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player)
                    if player.cardSum2 > 21:
                        player.split = False
                        return False
                    print("Hit,Hand2: {} and sum: {}".format(player.hand2,player.cardSum2))
                #Stand
                elif turn == 'S':
                    player.Stand()
                    return False
                    print("Stand")
                #Double
                elif turn == 'D':
                    player.Double(deck)
                    player.split = False
                    print("Double")
                    return False
        else:
            while True:
                (cursX,cursY,clickL,clickR) = getInput()
                #Hit
                if clickL and (cursX >= 485 and cursX <= 540) and (cursY >= 630 and cursY <= 657):
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player)
                    time.sleep(0.5)
                    if player.cardSum2 > 21:
                        player.split = False
                        return False
                    print("Hit,Hand2: {} and sum: {}".format(player.hand2,player.cardSum2))
                #Stand
                elif clickL and (cursX >= 637 and cursX <= 750) and (cursY >= 630 and cursY <= 657):
                    player.Stand()
                    time.sleep(0.5)
                    return False
                    print("Stand")
                #Double
                elif clickL and (cursX >= 265 and cursX <= 400) and (cursY >= 630 and cursY <= 657):
                    player.Double(deck)
                    player.split = False
                    time.sleep(0.5)
                    print("Double")
                    return False
                elif clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True

    def getAction():
        '''
        Get user action, i.e Hit, split etc
        '''
        print("Make your move. hit-1, stand-2, double-3, split-4?")
        print("phand: {}".format(player.hand))
        if not player.bot:
            while True:
                #TODO: MAKE GET INPUT FUNCTION
                (cursX,cursY,clickL,clickR) = getInput()
                #Hit
                if clickL and (cursX >= 485 and cursX <= 540) and (cursY >= 630 and cursY <= 657):
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player)
                    time.sleep(0.5)
                    if player.cardSum > 21:
                        return False
                    print("Hit: {}".format(player.hand))
                #Stand
                elif clickL and (cursX >= 637 and cursX <= 750) and (cursY >= 630 and cursY <= 657):
                    player.Stand()
                    print("Stand")
                    time.sleep(0.5)
                    return False
                #Double
                elif clickL and (cursX >= 265 and cursX <= 400) and (cursY >= 630 and cursY <= 657):
                    player.Double(deck)
                    print("Double")
                    time.sleep(0.5)
                    return False
                #Split
                elif clickL and (cursX >= 835 and cursX <= 925) and (cursY >= 630 and cursY <= 657):
                    if (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        possible = player.Split(deck)
                        #skip if player cannot afford
                        if not possible:
                            time.sleep(0.5)
                            continue
                        print("Split")
                        cont = doSplit(deck,player)
                        #TODO: split draw function here
                        if cont:
                            return True
                        else:
                            time.sleep(0.5)
                            continue

                elif clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True
        else:
            while True:
                result = player.computeTurn(deck,dealer.hand)
                if result == 'H':
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player)
                    print("Hit: {}".format(player.hand))
                    if player.cardSum > 21:
                        return False
                elif result == 'S':
                    print("Stand: {}".format(player.cardSum))
                    player.Stand()
                    return False
                elif result == 'D':
                    player.Double(deck)
                    print("Double: {}".format(player.hand))
                    return False
                elif result == 'X':
                    if player.splitV == True:
                        #force hit if already split
                        player.Hit(deck)
                        drawCards(player,player.hand[-1])
                        updateStats(player)
                        if player.cardSum > 21:
                            return False
                    elif (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        player.Split(deck)
                        print("Split")
                        doSplit(deck,player)
                        player.Hit(deck)
                        drawCards(player,player.hand[-1])
                        updateStats(player)




    if player.money < 5:
        print("Broke")
        return

    if len(player.hand) < 2:
        player.Hit(deck)
        drawCards(player,player.hand[-1])
        updateStats(player)
        time.sleep(0.5)
        player.Hit(deck)
        drawCards(player,player.hand[-1])
        updateStats(player)
        time.sleep(0.5)
        print("Player Hand: {}, Sum {}".format(player.hand,player.cardSum))
        return
    cont = getAction()
    if cont:
        return True

def initDeck(deck):
    deck.newDeck(deckNum)
    deck.shuffle()
    return deck

def initGame(playCount,botCount,deckN,scrn):
    #reinitialize variables if we already played
    if len(playList) != 0:
        pCards.pop() #need extra pop because it is 1 longer
        for i in range(len(playList)):
            playList.pop()
            pCards.pop()

    deckNum = deckN
    dealer = Dealer()
    pCards.append(cardPile(0))
    screenL.append(scrn)
    #init players
    for i in range(playCount):
        player = Player(i)
        cPile = cardPile(i+1)
        playList.append(player)
        pCards.append(cPile)
        updateStats(player)
    # init bots
    for i in range(botCount):
        bot = Player(i+playCount,True)
        cPile = cardPile(i+playCount+1)
        playList.append(bot)
        pCards.append(cPile)
        updateStats(bot)

    deck = Deck() #init deck
    deck = initDeck(deck)
    return (deck,dealer)

def startRound(deck,dealer):
    for hand in pCards:
        hand.clearCard()

    for player in playList:
        updateStats(player)

    for x in playList:
        cont = getBet(x,deck)
        if cont:
            return False

    for player in playList:
        getPlayerTurn(player,deck,dealer)

    result = getDealerTurn(deck,dealer)
    #print("Dealer First card and Sum: {}".format(result))
    for i in range(len(playList)):
        player = playList[i]
        cont = getPlayerTurn(player,deck,dealer)
        if cont:
            return False
        print("Player {} Hand: {}".format(i,player.hand))

    result = getDealerTurn(deck,dealer)
    dSum = result[1]
    while dSum < 17:
        #case where dealer draws an Ace, goes over limit
        #but the script used doesnt check and will return a number under 17
        result = getDealerTurn(deck,dealer)
    #NOTE: dealer wins on 21, may need to change
    dealer.done = True
    if dSum == 21:
        print("Dealer Sum: {}".format(dSum))
        for i in range(len(playList)):
            player = playList[i]
            if player.broke:
                continue
            if player.splitV:
                player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            player.playerLoss()
            player.clearHand()
    elif dSum > 21:
        for i in range(len(playList)):
            player = playList[i]
            if player.broke:
                continue
            if player.splitV:
                if player.cardSum2 <= 21:
                    player.playerWin()
                else:
                    player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            if player.cardSum <= 21:
                player.playerWin()
            if player.cardSum > 21:
                player.playerLoss()
    elif dSum < 21:
        for i in range(len(playList)):
            player = playList[i]
            if player.broke:
                continue
            if player.splitV:
                if (player.cardSum2 > dSum) and (player.cardSum2 <= 21):
                    player.playerWin()
                else:
                    player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            if player.cardSum > dSum and (player.cardSum <= 21):
                player.playerWin()
            elif player.cardSum <= dSum or (player.cardSum > 21):
                player.playerLoss()
    return True
