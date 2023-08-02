
from objects import Player, Game
import time
from concurrent.futures import ProcessPoolExecutor

ITERATIONS = 10000          # How many iterations for our Monte Carlo-esque sim?
TEST_WAGERS = range(1, 21)  # What wagers do we want to test? Note that the right bound is exclusive
STARTING_BALANCE = 1000     # How much should the player start with. We'll hold this constant and vary the wagers.
GAMES_TO_PLAY = 100         # Actually measures a Martingale sequence, concluding with a player win


def main():
    start_time = time.perf_counter()

    # Utilize multi-threading via ProcessPoolExecutor to reduce run-time significantly
    # Each 'test' can be run independently as they don't influence each other.
    executor = ProcessPoolExecutor(max_workers=len(TEST_WAGERS))
    for result in executor.map(run_test, TEST_WAGERS):
        print(result)

    end_time = time.perf_counter()
    print(f"Analysis complete after {end_time - start_time:0.4f} seconds")


def run_test(wager):

    baseline_bank = 0
    resulting_bank = 0
    bust_counter = 0
    for i in range(0, ITERATIONS):

        player = Player(STARTING_BALANCE, wager)
        game = Game(player)

        bust = False
        bet = player.initial_bet
        game_count = 0
        while game_count <= GAMES_TO_PLAY and not bust:
            result = game.play(bet)
            if result == "WIN":
                bet = player.initial_bet
                game_count += 1
            elif result == "LOSE":
                bet = bet * 2
            elif result == "BUST":
                bust = True

        resulting_bank += player.current_balance
        baseline_bank += player.starting_balance
        if bust:
            bust_counter += 1

    result = f"""
_______________________
Results for {str(wager)} / {str(STARTING_BALANCE)}
Bust percentage: {str((bust_counter / ITERATIONS) * 100)}%
Baseline Bank:  {str(baseline_bank)}
Resulting Bank: {str(resulting_bank)}
GAIN/LOSS: {str(((resulting_bank - baseline_bank) / baseline_bank) * 100)}%
_______________________
"""

    return result


if __name__ == "__main__":
    main()
