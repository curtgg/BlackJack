from Deck import Deck
from random import randrange

class Player:
    def __init__(self,num,bot=False):
        #init all necessary variables for the class
        #pass true if player is an AI
        #num is players position in the pList during the game
        self.num = num
        self.hand = []
        self.money = 500
        self.bet = 5
        self.split = False #handles split hitting
        self.splitV = False #handles split case after hitting is over
        self.cardSum = 0 #sum of players hand 1
        self.cardSum2 = 0
        self.broke = False #if broke true turn is skipped
        self.ace = False #ace of main hand
        self.ace2 = False #ace of split hand
        self.bet2 = 0
        self.bot = bot

    def clearHand(self):
        #clears the players hand at
        #end of a round and reinitializes some variables
        del self.hand
        self.hand = []
        if self.split:
            del self.hand2
        self.bet = 5
        self.split = False
        self.splitV = False
        self.cardSum = 0
        self.cardSum2 = 0
        self.ace = False
        self.ace2 = False
        self.bet2 = 0


    def Hit(self,deck):
        #hits card to player hand
        letters = {'A','J','K','Q'}
        card = deck.draw() #draw from deck
        cVal = card[1]
        #get value of card
        #and add to players sum
        if cVal in letters:
            if cVal == 'A':
                #add 11 set ace to true
                if self.split:
                    #if player has a split hand and is not finished hitting to it
                    self.cardSum2 += 11
                    self.ace2 = True
                else:
                    #otherwise add to main hand
                    self.cardSum += 11
                    self.ace = True
            else:
                #add to split if player isnt finished with that hand
                if self.split:
                    #if not an ace and in letters it is 10 val
                    self.cardSum2 += 10
                else:
                    self.cardSum += 10
        else:
            if self.split:
                #add val to sum
                self.cardSum2 += int(cVal)
            else:
                self.cardSum += int(cVal)
        #if we go over 21 after adding, if we have an ace we are allowed to subtract 10
        if ((self.cardSum > 21) and (self.ace == True)):
            self.cardSum -= 10
            self.ace = False
        #for the split hand aswell
        if self.split:
            if ((self.cardSum2 > 21) and (self.ace2 == True)):
                self.cardSum2 -= 10
                self.ace2 = False
        #adds card to respective hand
        if self.split:
            self.hand2.append(card)
        else:
            self.hand.append(card)

    def Stand(self):
        #if we stand on a split, set split to false so that we stop
        #adding cards to that hand
        if self.split:
            self.split = False
            self.splitV = True


    def Double(self,deck):
        #operates the same as the hit function except doubles the respective bet
        letters = {'A','J','K','Q'}
        card = deck.draw()
        cVal = card[1]
        if cVal in letters:
            if cVal == 'A':
                if self.split:
                    self.cardSum2 += 11
                    self.ace2 == True
                else:
                    self.cardSum += 11
                    self.ace == True
            else:
                if self.split:
                    self.cardSum2 += 10
                else:
                    self.cardSum += 10
        else:
            if self.split:
                self.cardSum2 += int(cVal)
            else:
                self.cardSum += int(cVal)
        if (self.cardSum > 21) and (self.ace == True):
            self.cardSum -= 10
            self.ace = False
        if self.split:
            if ((self.cardSum2 > 21) and (self.ace2 == True)):
                self.cardSum2 -= 10
                self.ace2 = False

        if self.split:
            self.hand2.append(card)
        else:
            self.hand.append(card)
        if self.split:
            self.bet2 *= 2
        else:
            self.bet *= 2

    def Split(self,deck):
        #splits are always handled before the main hand
        #splits the players hand into a second one, only possible if they have 2 of the
        #same card
        #check to ensure we have enough money
        if (self.money-(self.bet*2)) < 0:
            return False
        #if splitting is possible
        if (len(self.hand) == 2) and (self.hand[0][1] == self.hand[1][1]):
            #set split variables to true
            self.split = True
            self.splitV = True
            self.bet2 = self.bet #sets second bet to be the same
            card = self.hand[-1] #grabs second card
            del self.hand[-1] #deletes it
            #unique case of double aces
            if self.hand[0][1] == "A":
                self.cardSum2 = 11
                self.cardSum = 11
                self.ace = True
                self.ace2 = True
            else:
                #add half the total sum to the respective sum
                self.cardSum2 += (self.cardSum/2)
                self.cardSum -= (self.cardSum/2)
            #add card to hand
            self.hand2 = []
            self.hand2.append(card)
            return True


    def playerWin(self):
        #if player wins we run this function
        #if split hand wins we add the second bet to the cash stack
        if self.splitV:
            self.money += self.bet2
            self.split = False
            self.splitV = False
        else:
            #if main hand wins we add the bet to the cash
            self.money += (self.bet)
            self.clearHand() #clear hand
        print("Win, Player Money: {}".format(self.money))

    def playerLoss(self):
        """
        Player split loss/win is always handled first

        """
        #subtract the players second bet if split hand loses
        if self.splitV:
            self.money -= self.bet2
            self.split = False
            self.splitV = False
        else:
            #if main hand loses subtract bet
            self.money -= (self.bet)
            self.clearHand() #only want to clear hand if split dealt with
        if self.money <= 0:
            #if we run out of money, broke set to true
            self.broke = True
        print("Loss, Player Money: {}".format(self.money))


    def computeBet(self,deck):
        '''
        Using the card count of the deck, the AI attempts to create a bet..
        if count is high
        Args:
            self - player object as a bot
            deck - Deck class pre initialized
        '''
        count = deck.getCount()
        confidence = randrange(1,4) # for use later

        #if money is running low we use safe bets
        if self.money < 25:
            self.bet = 5
            return
        while True:
            #otherwise comput a bet based on the card count of the deck
            if count < -2:
                self.bet = 5*confidence
                #bet very low
            elif count < 0:
                self.bet = 10*confidence
                #bet low
            elif count < 3:
                self.bet = 15*confidence
                #bet neutral
            elif count < 5:
                self.bet = 20*confidence
                #bet high
            elif count >= 6:
                self.bet = 25*confidence
                #bet very high
            if self.money - self.bet < 0:
                continue
            else:
                return

    def computeTurn(self,deck,hand):
        '''
        Computes the player turn and returns the hand of which the
        optimal turn is and should be played.

        '''
        letters = {'J','K','Q'}
        #get players sum and ace value
        if self.split:
            cSum = int(self.cardSum2)
            ace = self.ace2
        else:
            cSum = int(self.cardSum)
            ace = self.ace
        #get card value
        dVal = hand[0][1]
        # we havent split and len of 2. try to split
        if not self.splitV:
            if (self.hand[0][1] == self.hand[1][1] and (len(self.hand) == 2)):
                #never split 2 10's
                if self.hand[0][1] in letters:
                    pass
                else:
                    #if split is possible, find split turn
                    turn = table[(self.hand[0][1],dVal)]
                    return turn
        #hit if lessthan 9 as there is no reason not to
        if cSum <= 8:
            turn = 'H'
            return turn
        #otherwise if not ace and greater than 17 we stand
        if cSum >=17 and not ace:
            turn = 'S'
            return turn
            #maybe splitV
        #if we have an ace, soft hand
        if ace:
            #stand at 19
            if cSum >= 19:
                turn = 'S'
            #otherwise
            else:
                #computer turn from soft values
                turn = table[((cSum,'S'),dVal)]
            print("Soft: {}".format(turn))
            return turn
        else:
            #otherwise just put sum into table and find normal result
            turn = table[(cSum,dVal)]
            return turn


class Dealer:
        def __init__(self):
            #init variables
            self.hand = []
            self.cardSum = 0
            self.ace = False
            self.done = False
            self.split = False

        def clearHand(self):
            #reset variables and clear hand
            del self.hand
            self.hand = []
            self.cardSum = 0
            self.ace = False
            self.done = False

        def draw(self,deck):
            #draw a card from the deck
            letters = {'A','J','K','Q'}
            card = deck.draw()
            cVal = card[1]
            if cVal in letters:
                if cVal == 'A':
                    self.cardSum += 11
                    self.ace = True
                else:
                    self.cardSum += 10
            else:
                self.cardSum += int(cVal) # add sum
            #dealer can go over 21 then subtract ten
            if (self.cardSum > 21) and (self.ace == True):
                self.cardSum -= 10
                self.ace = False
            self.hand.append(card)



#DICT WHICH DEFINES PROBABILITY TABLE FOR BOT MOVES
#FORMAT (playerSum,dealerCard):Optimal Move
#NOTE:ALL MOVE FOR PLAYER HAND >=17 ARE STAND AND IS NOT INCLUDED IN TABLE**
#NOTE: S: Stand, H:Hit, X:Split
table = {
(16,'2'):'S',(16,'3'):'S',(16,'4'):'S',(16,'5'):'S',(16,'6'):'S',(16,'7'):'H',(16,'8'):'H',
(16,'9'):'H',(16,'10'):'H',(16,'J'):'H',(16,'K'):'H',(16,'Q'):'H',(16,'A'):'H',

(15,'2'):'S',(15,'3'):'S',(15,'4'):'S',(15,'5'):'S',(15,'6'):'S',(15,'7'):'H',(15,'8'):'H',
(15,'9'):'H',(15,'10'):'H',(15,'J'):'H',(15,'K'):'H',(15,'Q'):'H',(15,'A'):'H',

(14,'2'):'S',(14,'3'):'S',(14,'4'):'S',(14,'5'):'S',(14,'6'):'S',(14,'7'):'H',(14,'8'):'H',
(14,'9'):'H',(14,'10'):'H',(14,'J'):'H',(14,'K'):'H',(14,'Q'):'H',(14,'A'):'H',

(13,'2'):'S',(13,'3'):'S',(13,'4'):'S',(13,'5'):'S',(13,'6'):'S',(13,'7'):'H',(13,'8'):'H',
(13,'9'):'H',(13,'10'):'H',(13,'J'):'H',(13,'K'):'H',(13,'Q'):'H',(13,'A'):'H',

(12,'2'):'H',(12,'3'):'S',(12,'4'):'S',(12,'5'):'S',(12,'6'):'S',(12,'7'):'H',(12,'8'):'H',
(12,'9'):'H',(12,'10'):'H',(12,'J'):'H',(12,'K'):'H',(12,'Q'):'H',(12,'A'):'H',

(11,'2'):'D',(11,'3'):'D',(11,'4'):'D',(11,'5'):'D',(11,'6'):'D',(11,'7'):'D',(11,'8'):'D',
(11,'9'):'D',(11,'10'):'H',(11,'J'):'H',(11,'K'):'H',(11,'Q'):'H',(11,'A'):'H',

(10,'2'):'D',(10,'3'):'D',(10,'4'):'D',(10,'5'):'D',(10,'6'):'D',(10,'7'):'D',(10,'8'):'D',
(10,'9'):'D',(10,'10'):'H',(10,'J'):'H',(10,'K'):'H',(10,'Q'):'H',(10,'A'):'H',

(9,'2'):'D',(9,'3'):'D',(9,'4'):'D',(9,'5'):'D',(9,'6'):'D',(9,'7'):'H',(9,'8'):'H',
(9,'9'):'H',(9,'10'):'H',(9,'J'):'H',(9,'K'):'H',(9,'Q'):'H',(9,'A'):'H',

##BELOW ARE COMBO'S WHERE PLAYER HAS AN ACE AND THEREFORE HAS A SOFT HAND
## FORMAT CHANGES TO ((playerSum,'S'),dealerCard) : Optimal Move
##Specifically if player ace is TRUE

((18,'S'),'2'):'S',((18,'S'),'3'):'D',((18,'S'),'4'):'D',((18,'S'),'5'):'D',((18,'S'),'D'):'S',
((18,'S'),'7'):'S',((18,'S'),'8'):'S',((18,'S'),'9'):'H',((18,'S'),'10'):'H',((18,'S'),'J'):'H',
((18,'S'),'K'):'H',((18,'S'),'Q'):'H',((18,'S'),'A'):'H',

((17,'S'),'2'):'H',((17,'S'),'3'):'D',((17,'S'),'4'):'D',((17,'S'),'5'):'D',((17,'S'),'6'):'D',
((17,'S'),'7'):'H',((17,'S'),'8'):'H',((17,'S'),'9'):'H',((17,'S'),'10'):'H',((17,'S'),'J'):'H',
((17,'S'),'K'):'H',((17,'S'),'Q'):'H',((17,'S'),'A'):'H',

((16,'S'),'2'):'H',((16,'S'),'3'):'H',((16,'S'),'4'):'D',((16,'S'),'5'):'D',((16,'S'),'6'):'D',
((16,'S'),'7'):'H',((16,'S'),'8'):'H',((16,'S'),'9'):'H',((16,'S'),'10'):'H',((16,'S'),'J'):'H',
((16,'S'),'K'):'H',((16,'S'),'Q'):'H',((16,'S'),'A'):'H',

((15,'S'),'2'):'H',((15,'S'),'3'):'H',((15,'S'),'4'):'D',((15,'S'),'5'):'D',((15,'S'),'6'):'D',
((15,'S'),'7'):'H',((15,'S'),'8'):'H',((15,'S'),'9'):'H',((15,'S'),'10'):'H',((15,'S'),'J'):'H',
((15,'S'),'K'):'H',((15,'S'),'Q'):'H',((15,'S'),'A'):'H',

((14,'S'),'2'):'H',((14,'S'),'3'):'H',((14,'S'),'4'):'H',((14,'S'),'5'):'D',((14,'S'),'6'):'D',
((14,'S'),'7'):'H',((14,'S'),'8'):'H',((14,'S'),'9'):'H',((14,'S'),'10'):'H',((14,'S'),'J'):'H',
((14,'S'),'K'):'H',((14,'S'),'Q'):'H',((14,'S'),'A'):'H',

((13,'S'),'2'):'H',((13,'S'),'3'):'H',((13,'S'),'4'):'H',((13,'S'),'5'):'D',((13,'S'),'6'):'D',
((13,'S'),'7'):'H',((13,'S'),'8'):'H',((13,'S'),'9'):'H',((13,'S'),'10'):'H',((13,'S'),'J'):'H',
((13,'S'),'K'):'H',((13,'S'),'Q'):'H',((13,'S'),'A'):'H',
###ABOVE ARE SOFT HANDS
## BELOW ARE PAIR CARDS
##SINCE S DENOTES A STAND X DENTOES SPLIT
#Format NOTE:only if 2 cards are same...(str(double card),dealercard):"X"
('A','2'):'X',('A','3'):'X',('A','4'):'X',('A','5'):'X',('A','6'):'X',('A','7'):'X',
('A','8'):'X',('A','9'):'X',('A','10'):'X',('A','J'):'X',('A','K'):'X',('A','Q'):'X',('A','A'):'X',

('10','2'):'S',('10','3'):'S',('10','4'):'S',('10','5'):'S',('10','6'):'S',('10','7'):'S',
('10','8'):'S',('10','9'):'S',('10','10'):'S',('10','J'):'S',('10','K'):'S',('10','Q'):'S',('10','A'):'S',

('9','2'):'X',('9','3'):'X',('9','4'):'X',('9','5'):'X',('9','6'):'X',('9','7'):'S',
('9','8'):'X',('9','9'):'X',('9','10'):'S',('9','J'):'S',('9','K'):'S',('9','Q'):'S',('9','A'):'S',

('8','2'):'X',('8','3'):'X',('8','4'):'X',('8','5'):'X',('8','6'):'X',('8','7'):'X',
('8','8'):'X',('8','9'):'X',('8','10'):'H',('8','J'):'H',('8','K'):'H',('8','Q'):'H',('8','A'):'H',

('7','2'):'X',('7','3'):'X',('7','4'):'X',('7','5'):'X',('7','6'):'X',('7','7'):'X',
('7','8'):'H',('7','9'):'H',('7','10'):'S',('7','J'):'S',('7','K'):'S',('7','Q'):'S',('7','A'):'H',

('6','2'):'X',('6','3'):'X',('6','4'):'X',('6','5'):'X',('6','6'):'X',('6','7'):'H',
('6','8'):'H',('6','9'):'H',('6','10'):'H',('6','J'):'H',('6','K'):'H',('6','Q'):'H',('6','A'):'H',

('5','2'):'D',('5','3'):'D',('5','4'):'D',('5','5'):'D',('5','6'):'D',('5','7'):'D',
('5','8'):'D',('5','9'):'D',('5','10'):'H',('5','J'):'H',('5','K'):'H',('5','Q'):'H',('5','A'):'H',

('4','2'):'H',('4','3'):'H',('4','4'):'H',('4','5'):'H',('4','6'):'H',('4','7'):'H',
('4','8'):'H',('4','9'):'H',('4','10'):'H',('4','J'):'H',('4','K'):'H',('4','Q'):'H',('4','A'):'H',

('3','2'):'H',('3','3'):'H',('3','4'):'X',('3','5'):'X',('3','6'):'X',('3','7'):'X',
('3','8'):'X',('3','9'):'H',('3','10'):'H',('3','J'):'H',('3','K'):'H',('3','Q'):'H',('3','A'):'H',

('2','2'):'H',('2','3'):'X',('2','4'):'X',('2','5'):'X',('2','6'):'X',('2','7'):'X',
('2','8'):'H',('2','9'):'H',('2','10'):'H',('2','J'):'H',('2','K'):'H',('2','Q'):'H',('2','A'):'H'
##ABOVE ARE PAIR CARDS
        }
