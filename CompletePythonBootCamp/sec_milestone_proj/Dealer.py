import Cards

class Dealer:
    def __init__(self, name='Robot',money=0, hand=Cards.Cards):
        self.name  = name
        self.money = money
        self.bet   = 0
        self.hand  = hand
    
    def receiveBet(self, val):
        if (val < 1):
            return False
        else:
            self.bet = val
            self.money += val
            return True

    def giveBet(self):
        ret = 0
        ret = self.bet        
        self.money -= self.bet
        self.bet = 0
        return ret


    def currentBet(self):
        print(f"Bet: {self.bet}")

    def showHand(self):
        print(self.hand)

    def startingHand(self):
        print(self.hand.cardsList[0])
        print("? - ?")

    def __str__(self):
        return f"Dealer: {self.name}, Money: {self.money}"