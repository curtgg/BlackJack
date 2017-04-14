from Deck import Deck
from Player import Player, Dealer
import pygame
import time
from Cardpile import cardPile
playList = [] #list of players
screenOp = [] #list of screen options
pCards = [] #list of players hand drawing objects
black = (0,0,0) #colour of text
green = (4, 134, 21) #defines game board colour
Mfont = pygame.font.Font(None, 40) #get text font
sumD = Mfont.render("Dealers Sum:",0, black)#sum string

def updateStats(player,deck):
    '''
    Updates the players stats(sum, bet, etc) under their respective position using the cardPile class,
    also updates the card counter of the deck if enabled in options
    Args:
        Player - player object to have stats updated
        deck - deck object pre initialized
    '''
    #get pos to draw stats
    cPile = pCards[player.num+1]
    #draw stats at given position with given stats
    cPile.drawStats(player.money,player.bet,player.cardSum,player.cardSum2,player.splitV,screenOp[0])
    #if we want to draw count
    if screenOp[1] == True:
        drawCount(deck)
    pygame.display.flip() ##update display **very important**

def drawDealer(dealer,card):
    '''
    Draws the dealers card using the cardPile class to determine position
    Args:
        Dealer - dealer object
        card - Card to draw
    '''
    #cover old dealer sum
    pygame.draw.rect(screenOp[0],green,[670,80,40,40])
    #draw sum
    D = Mfont.render(str(dealer.cardSum),0, black)#sum string
    #get position to draw card
    cPile = pCards[0]
    cPile.drawCard(dealer,screenOp[0])
    #draw the card
    screenOp[0].blit(sumD,(490,90))
    screenOp[0].blit(D,(680,90))
    pygame.display.flip() ##update display **very important**

def drawCards(player,card):
    '''
    Draws the players card using the cardPile class to determine position
    Args:
        Player - player object
        card - Card to draw
    '''
    #get player pos to draw cards, +1 cuz dealer is 0
    cPile = pCards[player.num+1]
    #draw cards at that pos
    cPile.drawCard(player,screenOp[0])
    pygame.display.flip() ##update display **very important**

def drawCount(deck):
    '''
    Draws the card count of the deck
    Args:
        deck - deck object
    '''
    #draw rectangle to cover old card count
    pygame.draw.rect(screenOp[0],green,[0,10,200,30])
    #draw count
    word = Mfont.render("Card Count: " + str(int(deck.count/deck.deckN)),0,black)
    screenOp[0].blit(word,(0,10))

def getBet(player,deck):
    '''
    Gets the players bet. IF the player is a bot it computes it using the
    computeBet function. If the player is a player it waits for their input and
    them to click on the bet button.
    Args:
        Player - player object
        deck - deck object
    '''
    #no money to play
    if player.money < 5:
        return
    else:
        #if human
        if not player.bot:
            print("Whats your bet? Up: +5, Down: -5")
            while True:
                (cursX,cursY,clickL,clickR) = getInput()
                #click on 10 chip
                if (clickL or clickR) and (cursX >= 1005 and cursX <= 1065) and (cursY >=495 and cursY <=555):
                    #left click to increment
                    if clickL and ((player.money-player.bet) >= 10):
                        player.bet += 10
                        time.sleep(0.5)
                    #right click to decrement
                    elif clickR and ((player.bet) > 10):
                        player.bet -= 10
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #five chip
                elif (clickL or clickR) and (cursX >= 1080 and cursX <= 1140) and (cursY >=495 and cursY <=555):
                    #left click to increment
                    if clickL and ((player.money-player.bet) >= 5):
                        player.bet += 5
                        time.sleep(0.5)
                    #right click to decrement
                    elif clickR and ((player.bet) > 5):
                        player.bet -= 5
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #one chip
                elif (clickL or clickR) and (cursX >= 1042 and cursX <= 1102) and (cursY >=555 and cursY <=615):
                    #left click to increment
                    if clickL and ((player.money-player.bet) >= 1):
                        player.bet += 1
                        time.sleep(0.5)
                    #right click to decrement
                    elif clickR and ((player.bet) > 1):
                        player.bet -= 1
                        time.sleep(0.5)
                    print("Player Bet: {}".format(player.bet))
                #Back to main menu
                if clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True
                #when player clicks the bet button, we finish
                elif clickL and (cursX >= 1038 and cursX <= 1102) and (cursY >= 461 and cursY <=486):
                    return False
                #update players stats
                updateStats(player,deck)
        else:
            #NOTE: IF bot compute the bet
            time.sleep(1)
            player.computeBet(deck)
            updateStats(player,deck)
            print("Player Bet:{} and count: {}".format(player.bet,deck.count))


def getInput():
    '''
    Gets and returns user input. Such as their mouse click and position
    where it was clicked
    '''
    #gets player input
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
    Args:
        deck - Deck object, pre initialized
        dealer - dealer object
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

    #NOTE:wont hit on 17
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
    Gets the players turn. if bot automatically determines using the computeTurn,
    otherwise program waits for user input to finish their turn
    Args:
        player - Player object
        deck - deck object
        dealer - dealer object
    '''
    turnOver = False
    def doSplit(deck,player):
        print("Make your move for hand 2, hit-1, stand-2, double-3, split-4?")
        #NOTE:Absolutely zero support for more than 1 splits
        #handles the splits for both players and bots
        if player.bot:
            #if bot, deal second card immediately after split
            player.Hit(deck)
            drawCards(player,player.hand[-1])
            updateStats(player,deck)
            print("Player Hand2: {}".format(player.hand2))
            while True:
                #compute turn and handle similar to main LOOP
                #player cannot split a second time
                turn = player.computeTurn(deck,dealer.hand)
                #Hit
                if turn == 'H' or turn == 'X':
                    #force hit on a split, only 1 split allowed
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    time.sleep(1)
                    if player.cardSum2 > 21:
                        player.split = False
                        return False
                    print("Hit,Hand2: {} and sum: {}".format(player.hand2,player.cardSum2))
                #Stand
                elif turn == 'S':
                    player.Stand()
                    time.sleep(1)
                    return False
                    print("Stand")
                #Double
                elif turn == 'D':
                    player.Double(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    player.split = False
                    print("Double")
                    time.sleep(1)
                    return False
        else:
            while True:
                #same loop as first, minues the split function
                (cursX,cursY,clickL,clickR) = getInput()
                #Hit
                if clickL and (cursX >= 485 and cursX <= 540) and (cursY >= 630 and cursY <= 657):
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
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
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    player.split = False
                    time.sleep(0.5)
                    print("Double")
                    return False
                elif clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True

    def getAction():
        '''
        Get user action, i.e Hit, split etc
        update the players stats and screen after dealing a card
        '''
        print("Make your move. hit-1, stand-2, double-3, split-4?")
        print("player hand: {}, Sum: {}".format(player.hand,player.cardSum))
        #if player passed in is a real person
        if not player.bot:
            while True:
                #get input
                (cursX,cursY,clickL,clickR) = getInput()
                #sleep after player selection to prevent input spam
                #Hit
                if clickL and (cursX >= 485 and cursX <= 540) and (cursY >= 630 and cursY <= 657):
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
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
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    print("Double")
                    time.sleep(0.5)
                    return False
                #Split, check whether or not its possible
                elif clickL and (cursX >= 835 and cursX <= 925) and (cursY >= 630 and cursY <= 657):
                    if (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        possible = player.Split(deck)
                        pCards[player.num+1].splitCard(player,screenOp[0])
                        #skip if player cannot afford
                        if not possible:
                            time.sleep(0.5)
                            continue
                        print("Split")
                        cont = doSplit(deck,player)
                        if cont:
                            return True
                        else:
                            time.sleep(0.5)
                            continue

                elif clickL and (cursX >= 1075 and cursX <= 1200) and (cursY >=0 and cursY <=50):
                    return True
        else:
            while True:
                #compute the bots hand based off the given factors
                result = player.computeTurn(deck,dealer.hand)
                #result will return a string: H is hit, S is stand, D is double, X is split
                #sleep after to simulate some realism and so all turns arent instantaneous
                if result == 'H':
                    player.Hit(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    print("Hit: {}, Sum: {}".format(player.hand,player.cardSum))
                    time.sleep(1)
                    if player.cardSum > 21:
                        return False
                elif result == 'S':
                    print("Stand: {}, Sum: {}".format(player.hand,player.cardSum))
                    player.Stand()
                    time.sleep(1)
                    return False
                elif result == 'D':
                    player.Double(deck)
                    drawCards(player,player.hand[-1])
                    updateStats(player,deck)
                    print("Double: {}, Sum: {}".format(player.hand,player.cardSum))
                    time.sleep(1)
                    return False
                elif result == 'X':
                    if player.splitV == True:
                        #force hit if already split
                        player.Hit(deck)
                        drawCards(player,player.hand[-1])
                        updateStats(player,deck)
                        time.sleep(1)
                        if player.cardSum > 21:
                            return False
                    elif (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        player.Split(deck)
                        pCards[player.num+1].splitCard(player,screenOp[0])
                        print("Split")
                        doSplit(deck,player)
                        player.Hit(deck)
                        drawCards(player,player.hand[-1])
                        updateStats(player,deck)
                        time.sleep(1)



    #disregard if player cant afford minimum bet
    if player.money < 5:
        print("Broke")
        return

    #deal initial 2 cards then return
    if len(player.hand) < 2:
        player.Hit(deck)
        drawCards(player,player.hand[-1])
        updateStats(player,deck)
        time.sleep(0.5)
        player.Hit(deck)
        drawCards(player,player.hand[-1])
        updateStats(player,deck)
        time.sleep(0.5)
        print("Player Hand: {}, Sum {}".format(player.hand,player.cardSum))
        return
    #otherwise player had 2 cards already.. get their action
    cont = getAction()
    #cont is whether or not they have pressed the exit button
    if cont:
        return True

def initDeck(deck,deckNum):
    '''
    initializes the game deck
    Args:
        deck - deck object
        deckNum - number of decks specified in options
    '''
    #initialize deck
    deck.newDeck(deckNum)
    deck.shuffle()
    return deck

def initGame(playCount,botCount,deckN,scrn,showCount,startCash):
    '''
    Initializes game and deck according the the game optons
    Args:
        playCount - number of players
        botCount - number of bots
        deckN - number of decks
        scrn - screen to be drawn onto
        showCount - whether or not card count is to be displayed
        startCash - starting player money
    '''
    #reinitialize variables if we already played
    if len(playList) != 0:
        pCards.pop() #need extra pop because it is 1 longer
        for i in range(len(playList)):
            playList.pop()
            pCards.pop()

    deckNum = deckN
    #init dealer object
    dealer = Dealer()
    #append him to the his position of 0
    pCards.append(cardPile(0))
    #reinitialize screen options
    if len(screenOp) >= 2:
        screenOp[1] = showCount
    else:
        screenOp.append(scrn)
        screenOp.append(showCount)
    #init the deck
    deck = Deck() #init deck
    deck = initDeck(deck,deckN)
    #init players
    for i in range(playCount):
        player = Player(i)
        cPile = cardPile(i+1)
        player.money = startCash
        playList.append(player)
        pCards.append(cPile)
        updateStats(player,deck)
    # init bots
    for i in range(botCount):
        bot = Player(i+playCount,True)
        cPile = cardPile(i+playCount+1)
        bot.money = startCash
        playList.append(bot)
        pCards.append(cPile)
        updateStats(bot,deck)
    return (deck,dealer)

def startRound(deck,dealer):
    '''
    Starts the game round and computes players bets, turns, and
    then finishes by checking who wins and loses based on the scenario on the board
    Args:
        Deck - deck object
        dealer - dealer object
    '''
    #clear player card drawing object
    for hand in pCards:
        hand.clearCard()

    #update player information
    for player in playList:
        updateStats(player,deck)

    #get each players bet
    for x in playList:
        time.sleep(0.2)
        cont = getBet(x,deck)
        #if cont is true then player has exited game
        if cont:
            return False

    #get each players initial card dealing, ie the 2 cards you start with
    for player in playList:
        getPlayerTurn(player,deck,dealer)
    #get dealers initial 1 card
    result = getDealerTurn(deck,dealer)
    #get all players other turns
    for i in range(len(playList)):
        player = playList[i]
        cont = getPlayerTurn(player,deck,dealer)
        #if cont is true then player has exited
        if cont:
            return False
        print("Player {} Hand: {}".format(i,player.hand))
    #get dealers final moves
    result = getDealerTurn(deck,dealer)
    dSum = result[1]
    while dSum < 17:
        #case where dealer draws an Ace, goes over limit
        #but the script used doesnt check and will return a number under 17
        result = getDealerTurn(deck,dealer)
    #dealer is now done
    dealer.done = True
    #if sum is 21, everyone loses
    if dSum == 21:
        print("Dealer Sum: {}".format(dSum))
        for i in range(len(playList)):
            player = playList[i]
            #if broke disregard player
            if player.broke:
                continue
            #deal with split hand
            if player.splitV:
                player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            #deal with main hand
            player.playerLoss()
            player.clearHand()
    #if over 21, everyone wins as long as they didnt bust
    elif dSum > 21:
        #for each player
        for i in range(len(playList)):
            player = playList[i]
            if player.broke:
                continue
            #deal with split cards
            if player.splitV:
                if player.cardSum2 <= 21:
                    player.playerWin()
                else:
                    player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            #deal with main hand
            if player.cardSum <= 21:
                player.playerWin()
            if player.cardSum > 21:
                player.playerLoss()
    #if less than 21, some win some lose
    elif dSum < 21:
        for i in range(len(playList)):
            player = playList[i]
            if player.broke:
                continue
            #deal with split hand
            if player.splitV:
                if (player.cardSum2 > dSum) and (player.cardSum2 <= 21):
                    player.playerWin()
                else:
                    player.playerLoss()
            print("Player {} Hand and Sum: {}, {}".format(i,player.cardSum,player.hand))
            #deal with main hand
            if player.cardSum > dSum and (player.cardSum <= 21):
                player.playerWin()
            elif player.cardSum <= dSum or (player.cardSum > 21):
                player.playerLoss()
    return True
