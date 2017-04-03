from random import shuffle
#unshuffled deck of cards, Tuple is (Type(H,D,S,C),Value)
#used to initialize deck
cards = [

('H','A'),('H','2'),('H','3'),('H','4'),('H','5'),('H','6'),('H','7'),
('H','8'),('H','9'),('H','10'),('H','J'),('H','K'),('H','Q'),
('D','A'),('D','2'),('D','3'),('D','4'),('D','5'),('D','6'),('D','7'),
('D','8'),('D','9'),('D','10'),('D','J'),('D','K'),('D','Q'),
('C','A'),('C','2'),('C','3'),('C','4'),('C','5'),('C','6'),('C','7'),
('C','8'),('C','9'),('C','10'),('C','J'),('C','K'),('C','Q'),
('S','A'),('S','2'),('S','3'),('S','4'),('S','5'),('S','6'),('S','7'),
('S','8'),('S','9'),('S','10'),('S','J'),('S','K'),('S','Q'),

]


class Deck:
    def __init__(self):
        self._array = []

    #Add's n decks, 1 if no argument is given
    #these decks are ORDERED and should have
    #shuffle be called afterwards for an unordered deck
    #the order is as shown above in the cards list


    def newDeck(self,n=1):
        """
        Add's n decks, 1 if no argument is given
        these decks are ORDERED and should have
        shuffle be called afterwards for an unordered deck
        the order is as shown above in the cards list

        Args:
            n - Number of decks to add to total deck, each deck is 52 cards
            default value is 1 if none specified
        """
        while n > 0:
            for i in cards:
                self._array.append(i)
            n -= 1


    def shuffle(self):
        """
        shuffle the elements of the deck
        should always be called after adding newDeck

        """
        shuffle(self._array)

    def add(self, val):
        """
        Add's a card to the deck, this functions purpose is for
        initializing the deck, probably wont be used otherwise

        """
        self._array.append((val))

    def draw(self):
        '''
        draw's a single card

        '''
        if not self._array:
            raise RuntimeError("Attempt to draw an empty deck")
        val = self._array[-1] #get top card
        del self._array[-1]
        return val

    def deckSize(self):
        '''
        returns Deck Size

        '''
        return len(self._array)

    def burnCards(self,n=1):
        '''
        Burns n amount of cards, default 1 if no argument given
        burnt card is not returned

        Args:
            n - number of cards to burn
        '''
        for i in range(n):
            draw = self.draw()

def testDeck():
    deck = Deck()
    deck.newDeck(3)
    deck.shuffle()
    print("Before Burn: {}".format(deck.deckSize()))
    deck.burnCards(52)
    print("After Burn: {}".format(deck.deckSize()))
    for i in range(deck.deckSize()):
        print(deck.draw())
        pass

#uncomment to run test cases
testDeck()
