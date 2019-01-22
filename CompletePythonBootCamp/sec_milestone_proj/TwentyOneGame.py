import Cards
import Player
import Dealer

class TwentyOneGame:
    def __init__(self, human=Player.Player(), computer=Dealer.Dealer(), deck=Cards.Deck()):
        self.human    = human
        self.computer = computer
        self.deck     = deck
        self.turn     = 1 # 1- Human Player turn, 2- Computer Dealer turn

    def startGame(self):
        print("Twenty One - Let's begin!")
        print(self.human)
        print(self.computer)

        bet = -1
        while(not self.human.bet(bet)):
            try:
                bet = int(input(f"How much do you bet {self.human.name}? "))
            except:
                print("You can't bet this :(, try again")

        # Must shuffle cards here
        self.deck.shuffle()

        # Must give cards here
        self.computer.hand = self.deck.newHand()
        self.human.hand = self.deck.newHand()

        print(f"Dealer {self.computer.name} cards: ")
        self.computer.startingHand()
        print(f"Player {self.human.name} cards: ")
        self.human.startingHand()
        print(f"Player total: {self.human.hand.total()}")

        endGame = False
        again = True
        choice = 0
        while again:
            choice = int(input("What do you do? [1-Hit, 2-Stay] > "))
            if choice == 1:
                print("Player chooses to Hit...")
                self.human.hand.receiveCard(self.deck.getCard())
                again = True
            elif choice == 2:
                print("Player chooses to stay...")
                again = False
            else:
                print("Invalid action!")
                again = True
            
            print(f"Player {self.human.name} cards: ")
            self.human.showHand()
            print(f"Player total: {self.human.hand.total()}")

            if self.human.hand.total() > 21:
                print(f"Player {self.human.name} has lost!")
                endGame = True
                break
        
        if not endGame:
            again = True

            while again:
                print(f"Dealer {self.computer.name} time!")
                self.computer.hand.receiveCard(self.deck.getCard())
                print(f"Dealer {self.computer.name} cards: ")
                self.computer.showHand()
                print(f"Dealer total: {self.computer.hand.total()} \n")

                if self.computer.hand.total() > 21:
                    print(f"Player {self.human.name} won!")
                    self.human.putMoney(self.computer.giveBet())
                    endGame = True
                    again = False
                elif self.computer.hand.total() > self.human.hand.total():
                    print(f"Player {self.human.name} has lost!")
                    endGame = True
                    again = False
        
        print("Twenty One - The End!")
