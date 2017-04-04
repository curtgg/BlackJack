from Deck import Deck
class Player:
    def __init__(self):
        self.hand = []
        self.money = 500
        self.bet = 5
        self.split = False
        self.cardSum = 0
        self.cardSum2 = 0
        self.broke = False
        self.ace = False
        self.ace2 = False
        self.bet2 = 0

    def clearHand(self):
        del self.hand
        self.hand = []
        if self.split:
            del self.hand2
        self.bet = 5
        self.split = False
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
        pass

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
        if (len(self.hand) == 2) and (self.hand[0][1] == self.hand[1][1]):
            self.split = True
            self.splitV = True
            self.bet2 = self.bet
            card = self.hand[-1]
            del self.hand[-1]
            self.hand2 = []
            self.hand2.append(card)


    def playerWin(self):
        if self.split:
            self.money += self.bet2
            self.split = False
        else:
            self.money += (self.bet)
            self.clearHand()
        print("Win, Player Money: {}".format(self.money))

    def playerLoss(self):
        if self.split:
            self.money -= self.bet2
            self.split = False
        else:
            self.money -= (self.bet)
            self.clearHand() #only want to clear hand if split dealt with
        if self.money <= 0:
            self.broke = True
        print("Loss, Player Money: {}".format(self.money))


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
