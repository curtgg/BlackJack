from Deck import Deck
from random import randrange

class Player:
    def __init__(self,bot=False):
        self.hand = []
        self.money = 500
        self.bet = 5
        self.split = False
        self.splitV = False
        self.cardSum = 0
        self.cardSum2 = 0
        self.broke = False
        self.ace = False
        self.ace2 = False
        self.bet2 = 0
        if bot == True:
            self.bot = True
        else:
            self.bot = False

    def clearHand(self):
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
        letters = {'A','J','K','Q'}
        card = deck.draw()
        cVal = card[1]
        if cVal in letters:
            if cVal == 'A':
                if self.split:
                    self.cardSum2 += 11
                    self.ace2 = True
                else:
                    self.cardSum += 11
                    self.ace = True
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
        if ((self.cardSum > 21) and (self.ace == True)):
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

    def Stand(self):
        if self.split:
            self.split = False
            self.splitV = True


    def Double(self,deck):
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

    #TODO:check that player cant split if money isnt suffiecient
    def Split(self,deck):
        if (self.money-(self.bet*2)) < 0:
            return False
        if (len(self.hand) == 2) and (self.hand[0][1] == self.hand[1][1]):
            self.split = True
            self.splitV = True
            self.bet2 = self.bet
            card = self.hand[-1]
            del self.hand[-1]
            #unique case of double aces
            if self.hand[0][1] == "A":
                self.cardSum2 = 11
                self.cardSum = 11
                self.ace = True
                self.ace2 = True
            else:
                self.cardSum2 += (self.cardSum/2)
                self.cardSum -= (self.cardSum/2)
            self.hand2 = []
            self.hand2.append(card)
            return True


    def playerWin(self):
        if self.splitV:
            self.money += self.bet2
            self.split = False
            self.splitV = False
        else:
            self.money += (self.bet)
            self.clearHand()
        print("Win, Player Money: {}".format(self.money))

    def playerLoss(self):
        """
        PLAYER SPLIT HAND DOES FIRST ALWAYS

        """
        if self.splitV:
            self.money -= self.bet2
            self.split = False
            self.splitV = False
        else:
            self.money -= (self.bet)
            self.clearHand() #only want to clear hand if split dealt with
        if self.money <= 0:
            self.broke = True
        print("Loss, Player Money: {}".format(self.money))


    def computeBet(self,deck):
        '''
        Using the card count of the deck, the AI attempts to create a bet..
        if count is high
        Args:
            deck - Deck class pre initialized

        TODO:
        Have bot consider his cash stack aswell as the card count
        when making the decision.
        Work on making actual decisions rather than RNG based off count
        maybe some sort of bet scaling based off the count?
        These values need to be refined
        '''
        #TODO:Choose better values for betting
        count = deck.getCount()
        randNum = randrange(0,10) # for use later
        #NOTE:Basic cases
        if count < -2:
            self.bet = 5
            #bet very low
        elif count < 0:
            self.bet = 10
            #bet low
        elif count < 3:
            self.bet = 15
            #bet neutral
        elif count < 5:
            self.bet = 20
            #bet high
        elif count > 6:
            self.bet = 25
            #bet very high

    def computeTurn(self,deck,hand):
        '''
        Computes the player turn and returns the hand of which the
        optimal turn is and should be played.
        TODO: finish function
        -handle splits
        -handle when player has splitV
        -handle aces
        more
        '''
        letters = {'J','K','Q'}
        #maybe splitV
        if self.split:
            cSum = int(self.cardSum2)
            ace = self.ace
        else:
            cSum = int(self.cardSum)
            ace = self.ace2
        dVal = hand[0][1]
        if not self.splitV:
            if (self.hand[0][1] == self.hand[1][1]):
                if self.hand[0][1] in letters:
                    pass
                else:
                    #if split is possible
                    turn = table[(self.hand[0][1],dVal)]
                    return turn
        if cSum < 5:
            turn = 'H'
            return turn
        if cSum <= 12 and ace:
            turn = 'H'
            return turn
        if cSum >=17 and not ace:
            turn = 'S'
            return turn
            #maybe splitV
        if ace:
            #if soft hand
            if cSum > 20:
                turn = 'S'
            else:
                turn = table[((cSum,'S'),dVal)]
            print("Soft: {}".format(turn))
            return turn
        else:
            turn = table[(cSum,dVal)]
            return turn


class Dealer:
        def __init__(self):
            self.hand = []
            self.cardSum = 0
            self.ace = False
            self.done = False

        def clearHand(self):
            del self.hand
            self.hand = []
            self.cardSum = 0
            self.ace = False
            self.done = False

        def draw(self,deck):
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
                self.cardSum += int(cVal)
            if (self.cardSum > 21) and (self.ace == True):
                self.cardSum -= 10
                self.ace = False
            self.hand.append(card)



#DICT WHICH DEFINES PROBABILITY TABLE FOR HINTS AND BOT MOVES
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

(8,'2'):'H',(8,'3'):'H',(8,'4'):'H',(8,'5'):'H',(8,'6'):'H',(8,'7'):'H',(8,'8'):'H',
(8,'9'):'H',(8,'10'):'H',(8,'J'):'H',(8,'K'):'H',(8,'Q'):'H',(8,'A'):'H',

(7,'2'):'H',(7,'3'):'H',(7,'4'):'H',(7,'5'):'H',(7,'6'):'H',(7,'7'):'H',(7,'8'):'H',
(7,'9'):'H',(7,'10'):'H',(7,'J'):'H',(7,'K'):'H',(7,'Q'):'H',(7,'A'):'H',

(6,'2'):'H',(6,'3'):'H',(6,'4'):'H',(6,'5'):'H',(6,'6'):'H',(6,'7'):'H',(6,'8'):'H',
(6,'9'):'H',(6,'10'):'H',(6,'J'):'H',(6,'K'):'H',(6,'Q'):'H',(6,'A'):'H',

(5,'2'):'H',(5,'3'):'H',(5,'4'):'H',(5,'5'):'H',(5,'6'):'H',(5,'7'):'H',(5,'8'):'H',
(5,'9'):'H',(5,'10'):'H',(5,'J'):'H',(5,'K'):'H',(5,'Q'):'H',(5,'A'):'H',

##BELOW ARE COMBO'S WHERE PLAYER HAS AN ACE AND THEREFORE HAS A SOFT HAND
## FORMAT CHANGES TO ((playerSum,'S'),dealerCard) : Optimal Move
##Specifically if player ace is TRUE
((20,'S'),'2'):'S',((20,'S'),'3'):'S',((20,'S'),'4'):'S',((20,'S'),'5'):'S',((20,'S'),'6'):'S',
((20,'S'),'7'):'S',((20,'S'),'8'):'S',((20,'S'),'9'):'S',((20,'S'),'10'):'S',((20,'S'),'J'):'S',
((20,'S'),'K'):'S',((20,'S'),'Q'):'S',((20,'S'),'A'):'S',

((19,'S'),'2'):'S',((19,'S'),'3'):'S',((19,'S'),'4'):'S',((19,'S'),'5'):'S',((19,'S'),'6'):'S',
((19,'S'),'7'):'S',((19,'S'),'8'):'S',((19,'S'),'9'):'S',((19,'S'),'10'):'S',((19,'S'),'J'):'S',
((19,'S'),'K'):'S',((19,'S'),'Q'):'S',((19,'S'),'A'):'S',

((18,'S'),'2'):'S',((18,'S'),'3'):'S',((18,'S'),'4'):'S',((18,'S'),'5'):'S',((18,'S'),'6'):'S',
((18,'S'),'7'):'S',((18,'S'),'8'):'S',((18,'S'),'9'):'S',((18,'S'),'10'):'S',((18,'S'),'J'):'S',
((18,'S'),'K'):'S',((18,'S'),'Q'):'S',((18,'S'),'A'):'S',

((17,'S'),'2'):'H',((17,'S'),'3'):'H',((17,'S'),'4'):'H',((17,'S'),'5'):'H',((17,'S'),'6'):'H',
((17,'S'),'7'):'H',((17,'S'),'8'):'H',((17,'S'),'9'):'H',((17,'S'),'10'):'H',((17,'S'),'J'):'H',
((17,'S'),'K'):'H',((17,'S'),'Q'):'H',((17,'S'),'A'):'H',

((16,'S'),'2'):'H',((16,'S'),'3'):'H',((16,'S'),'4'):'H',((16,'S'),'5'):'H',((16,'S'),'6'):'H',
((16,'S'),'7'):'H',((16,'S'),'8'):'H',((16,'S'),'9'):'H',((16,'S'),'10'):'H',((16,'S'),'J'):'H',
((16,'S'),'K'):'H',((16,'S'),'Q'):'H',((16,'S'),'A'):'H',

((15,'S'),'2'):'H',((15,'S'),'3'):'H',((15,'S'),'4'):'H',((15,'S'),'5'):'H',((15,'S'),'6'):'H',
((15,'S'),'7'):'H',((15,'S'),'8'):'H',((15,'S'),'9'):'H',((15,'S'),'10'):'H',((15,'S'),'J'):'H',
((15,'S'),'K'):'H',((15,'S'),'Q'):'H',((15,'S'),'A'):'H',

((14,'S'),'2'):'H',((14,'S'),'3'):'H',((14,'S'),'4'):'H',((14,'S'),'5'):'H',((14,'S'),'6'):'H',
((14,'S'),'7'):'H',((14,'S'),'8'):'H',((14,'S'),'9'):'H',((14,'S'),'10'):'H',((14,'S'),'J'):'H',
((14,'S'),'K'):'H',((14,'S'),'Q'):'H',((14,'S'),'A'):'H',

((13,'S'),'2'):'H',((13,'S'),'3'):'H',((13,'S'),'4'):'H',((13,'S'),'5'):'H',((13,'S'),'6'):'H',
((13,'S'),'7'):'H',((13,'S'),'8'):'H',((13,'S'),'9'):'H',((13,'S'),'10'):'H',((13,'S'),'J'):'H',
((13,'S'),'K'):'H',((13,'S'),'Q'):'H',((13,'S'),'A'):'H',
###ABOVE ARE SOFT HANDS
## BELOW ARE PAIR cards
##SINCE S DENOTES A STAND X DENTOES SPLIT
#Format NOTE:only if 2 cards are same...(double card,dealercard):"X"
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
