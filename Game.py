from Deck import Deck
from Player import Player, Dealer
import pygame

playCount = 0 #number of players
botCount = 1 #number of bots
deckNum = 150 #number of decks sepecified
playList = []

def getInput():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            return event.key
        if event.type == pygame.QUIT: sys.exit()

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

    #only if <1, as in start of round
    if len(dealer.hand) < 1:
        dealer.draw(deck)
        print("Dealer Hand: {}".format(dealer.hand))
        return (dealer.hand,dealer.cardSum)

    #NOTE:wont hit on 17, may need to change dependent
    #NOTE:on what we deside to do
    #dealer.draw(deck)
    print("Dealer Hand: {} and Sum: {}".format(dealer.hand,dealer.cardSum))
    while dealer.cardSum < 17 or (dealer.cardSum == 17 and dealer.ace):
        dealer.draw(deck)
        print("Dealer Hand: {} and Sum: {}".format(dealer.hand,dealer.cardSum))
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
            while True:
                turn = player.computeTurn(deck,dealer.hand)
                #Hit
                if turn == 'H' or turn == 'X':
                    #force hit on a split, only 1 split allowed
                    player.Hit(deck)
                    if player.cardSum2 > 21:
                        player.split = False
                        return True
                    print("Hit,Hand2: {} and sum: {}".format(player.hand2,player.cardSum2))
                #Stand
                elif turn == 'S':
                    player.Stand()
                    return True
                    print("Stand")
                #Double
                elif turn == 'D':
                    player.Double(deck)
                    player.split = False
                    print("Double")
                    return True
        else:
            while True:
                keyNum = getInput()
                #Hit
                if keyNum == pygame.K_1:
                    player.Hit(deck)
                    if player.cardSum2 > 21:
                        player.split = False
                        return True
                    print("Hit,Hand2: {} and sum: {}".format(player.hand2,player.cardSum2))
                #Stand
                if keyNum == pygame.K_2:
                    player.Stand()
                    return True
                    print("Stand")
                #Double
                if keyNum == pygame.K_3:
                    player.Double(deck)
                    player.split = False
                    print("Double")
                    return True

    def getBet():
        #no money to play
        if player.money < 5:
            return
        else:
            if not player.bot:
                print("Whats your bet? Up: +5, Down: -5")
                while True:
                    keyNum = getInput()
                    if keyNum == pygame.K_UP and (player.bet <= (player.money-5)):
                        player.bet += 5
                        print("Player Bet: {}".format(player.bet))
                    if keyNum == pygame.K_DOWN and (player.bet >= 10):
                        player.bet -= 5
                        print("Player Bet: {}".format(player.bet))
                    if keyNum == pygame.K_RETURN:
                        return
            else:
                #NOTE: IF bot compute the bet
                player.computeBet(deck)
                print("Player Bet:{} and count: {}".format(player.bet,deck.count))
    def getAction():
        '''
        Get user action, i.e Hit, split etc
        '''
        print("Make your move. hit-1, stand-2, double-3, split-4?")
        print("phand: {}".format(player.hand))
        if not player.bot:
            while True:
                #TODO: MAKE GET INPUT FUNCTION
                keyNum = getInput()
                #Hit
                if keyNum == pygame.K_1:
                    player.Hit(deck)
                    if player.cardSum > 21:
                        return True
                    print("Hit: {}".format(player.hand))
                #Stand
                if keyNum == pygame.K_2:
                    player.Stand()
                    return True
                    print("Stand")
                #Double
                if keyNum == pygame.K_3:
                    player.Double(deck)
                    print("Double")
                    return True
                #Split
                if keyNum == pygame.K_4:
                    #code may break here
                    if (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        player.Split(deck)
                        print("Split")
                        doSplit(deck,player)
        else:
            while True:
                result = player.computeTurn(deck,dealer.hand)
                if result == 'H':
                    player.Hit(deck)
                    print("Hit: {}".format(player.hand))
                    if player.cardSum > 21:
                        return True
                elif result == 'S':
                    print("Stand: {}".format(player.cardSum))
                    player.Stand()
                    return True
                elif result == 'D':
                    player.Double(deck)
                    print("Double: {}".format(player.hand))
                    return True
                elif result == 'X':
                    print('MAJOR KEY ALERT')
                    if player.splitV == True:
                        #force hit if already split
                        player.Hit(deck)
                        if player.cardSum > 21:
                            return True
                    elif (len(player.hand) == 2) and (player.hand[0][1] == player.hand[1][1]) and (player.splitV == False):
                        player.Split(deck)
                        print("Split")
                        doSplit(deck,player)
                        player.Hit(deck)




    if player.money < 5:
        print("Broke")
        return

    if len(player.hand) < 2:
        player.Hit(deck)
        player.Hit(deck)
        print("Player Hand: {}, Sum {}".format(player.hand,player.cardSum))
    getBet()
    turnOver = getAction()

def initDeck(deck):
    deck.newDeck(deckNum)
    deck.shuffle()
    return deck

def initGame():
    #Add players
    dealer = Dealer()
    for i in range(playCount):
        player = Player()
        playList.append(player)
    for i in range(botCount):
        bot = Player(True)
        playList.append(bot)
    deck = Deck() #init deck
    deck = initDeck(deck)
    return (deck,dealer)

def startRound(deck,dealer):
    result = getDealerTurn(deck,dealer)
    #print("Dealer First card and Sum: {}".format(result))
    for i in range(len(playList)):
        player = playList[i]
        getPlayerTurn(player,deck,dealer)
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
    return
#
#(deck,dealer) = initGame()
#while True:
#    startRound(deck,dealer)
