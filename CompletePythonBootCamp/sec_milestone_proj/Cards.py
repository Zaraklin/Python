import random

class Card:
    def __init__(self, cardValue, cardSuit):
        self.cardSuit = cardSuit

        if cardValue == 1:
            self.cardValue = cardValue
            self.cardType = "Ace"
        elif cardValue > 1 and cardValue <= 10:
            self.cardValue = cardValue
            self.cardType = "Number"
        elif cardValue == 11:
            self.cardValue = 10
            self.cardType = "Jack"
        elif cardValue == 12:
            self.cardValue = 10
            self.cardType = "Queen"
        elif cardValue == 13:
            self.cardValue = 10
            self.cardType = "King"
        else:
            self.cardValue = 0
            self.cardType = "Invalid Type"

    def specialAce(self, val):
        if self.cardType == "Ace" and (val == 1 or val == 11):
            self.cardValue = val
            return True
        else:
            return False

    def __str__(self):
        if self.cardType == "Number":
            return f"{self.cardValue} - {self.cardSuit}"
        else:
            return f"{self.cardType} - {self.cardSuit}"

class Deck:
    def __init__(self):
        cardList = []

        for x in range(0,3):
            if x == 0:
                rank = "Clubs"
            elif x == 1:
                rank = "Diamonds"
            elif x == 2:
                rank = "Hearts"
            elif x == 3:
                rank = "Spades"
            else:
                rank = "Invalid"
            for y in range(1,13):
                c = Card(y, rank)
                cardList.append(c)

        self.cardsList = cardList

    def shuffle(self):
        random.shuffle(self.cardsList)

    def newHand(self):
        hand = Cards()       

        for i in range(0,2):
            hand.receiveCard(self.cardsList.pop())

        return hand

    def getCard(self):
        if len(self.cardsList) > 0:
            return self.cardsList.pop()
        else:
            print("Deck has no more cards!")

class Cards:
    def __init__(self):
        self.cardsList = []
    
    def __str__(self):
        ret = ""
        
        for i in self.cardsList:
            ret += i.__str__() + "\n"

        return ret

    def receiveCard(self, card):
        self.cardsList.append(card)

    def total(self):
        tot = 0

        for i in self.cardsList:
            tot += i.cardValue

        return tot