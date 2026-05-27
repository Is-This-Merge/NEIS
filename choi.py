import random

class CroquetMatch:
    def __init__(self):
        self.currentTurn = 0
        self.isWin = False
        self.soldiers = []
        self.goals = []
        self.terrain = []

    def passTurn(self):
        self.currentTurn += 1
        print(f"Turn {self.currentTurn} passed.")
    
    def playTurn(self):
        # Simulate a turn of the game
        print(f"Playing turn {self.currentTurn}...")
        # Here you would implement the logic for a player's turn, such as moving soldiers, checking for goals, etc.
        # For demonstration purposes, we'll just randomly determine if the player wins.
        if random.random() < 0.1:  # 10% chance to win
            self.isWin = True
            print("Congratulations! You've won the match!")
        else:
            print("No win this turn. Keep playing!")