import Cards

class Player:
    def __init__(self, name='Jack', money=500, hand=Cards.Cards):
        self.name = name
        self.money = money
        self.hand = hand

    def bet(self, val):
        if (val > self.money):
            return False
        elif( val < 0):
            return False
        else:
            self.money -= val
            return True

    def putMoney(self, val):
        if (val < 0):
            return False
        else:
            self.money += val

    def showHand(self):
        print(self.hand)

    def startingHand(self):
        self.showHand()

    def __str__(self):
        return f"Player: {self.name}, Money: {self.money}"