import random


class Game:
    def __init__(self, player):
        self.player = player

    def play(self, wager):
        if wager > self.player.current_balance:
            return "BUST"

        # Remove the wager from the player's current balance
        self.player.current_balance -= wager

        result = random.randint(0, 36)
        multiplier = 0
        if result % 2 != 0:
            multiplier = 2

        # Add the winnings to the player's current balance
        self.player.current_balance += (multiplier * wager)

        game_outcome = "WIN" if multiplier > 0 else "LOSE"
        return game_outcome


class Player:

    def __init__(self, starting_balance, initial_bet):
        self.starting_balance = starting_balance
        self.current_balance = starting_balance
        self.initial_bet = initial_bet

    def __str__(self):
        return str(self.current_balance)