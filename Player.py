from Deck import Deck
class Player:
    def __init__(self):
        self.hand = []
        self.money = 500
        self.bet = 5
        self.split = False

    def clearHand():
        self.hand = []

    def addCard(self,card):
        self.hand.append(card)

    def Hit(self,deck):
        self.hand.append(deck.draw())

    def Stand(self):
        pass

    def Double(self,deck):
        self.hand.append(deck.draw())
        self.bet *= 2

    def Split(self,deck):
        #TODO: this will be complex
        #plan is to create a second hand for the player
        #treat it as its own entity
        pass

    def playerWin(self):
        pass

    def playerLoss(self):
        self.money -= self.bet
        pass
