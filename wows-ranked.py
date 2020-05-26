import random
import argparse
from collections import Counter
import matplotlib.pyplot as plt

# Defaults
DEFAULT_FIRST_RATE = 1 / 7  # chance to get 1st place in a battle
DEFAULT_WIN_RATE = 0.5  # chance to win a battle
DEFAULT_MAX_BATTLES = 10000  # maximum number of battles before simulation stops
DEFAULT_SIMULATION_RUNS = 5000  # number of times to run the simulation

# Season 16 rank information
ranks = {
    18: {
        'stars': 1,
        'irrevocable': True,
        'free-star': False
    },
    17: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    16: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    15: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    14: {
        'stars': 2,
        'irrevocable': False,
        'free-star': True
    },
    13: {
        'stars': 2,
        'irrevocable': False,
        'free-star': True
    },
    12: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    11: {
        'stars': 2,
        'irrevocable': False,
        'free-star': True
    },
    10: {
        'stars': 4,
        'irrevocable': False,
        'free-star': True
    },
    9: {
        'stars': 4,
        'irrevocable': False,
        'free-star': True
    },
    8: {
        'stars': 4,
        'irrevocable': False,
        'free-star': True
    },
    7: {
        'stars': 4,
        'irrevocable': False,
        'free-star': True
    },
    6: {
        'stars': 4,
        'irrevocable': False,
        'free-star': True
    },
    5: {
        'stars': 5,
        'irrevocable': False,
        'free-star': True
    },
    4: {
        'stars': 5,
        'irrevocable': False,
        'free-star': True
    },
    3: {
        'stars': 5,
        'irrevocable': False,
        'free-star': True
    },
    2: {
        'stars': 5,
        'irrevocable': False,
        'free-star': True
    },
    1: {
        'stars': 1,
        'irrevocable': True,
        'free-star': True
    }
}
start_rank = max(ranks.keys())
end_rank = min(ranks.keys())


def one_run(wr, fr, max_battles=DEFAULT_MAX_BATTLES):
    """
    Simulate battles required to complete ranked season.

    :param wr: win rate
    :param fr: first place rate
    :param max_battles: maximum battles before simulation ends (prevents infinite loops).
    :return: number of battles
    """
    battles = 0
    stars = 0
    simulated_rank = start_rank

    while simulated_rank != end_rank:
        battles += 1

        # Determine battle outcome
        if random.random() < wr:
            stars += 1
        elif random.random() < fr:  # best player doesn't lose star
            stars -= 1

        # Check if player moved up a rank
        if stars == ranks[simulated_rank]['stars']:
            simulated_rank -= 1  # move "up" a rank
            if ranks[simulated_rank]['free-star']:
                stars = 1  # get a free star for next rank
            else:
                stars = 0  # no free star

        # Check if a player moved down a rank
        if stars < 0:
            if ranks[simulated_rank]['irrevocable']:
                stars = 0
            else:
                simulated_rank += 1  # move "down" a rank
                stars = ranks[simulated_rank]['stars'] - 1  # 1 star away from next rank

        if battles > max_battles:
            break

    return battles


if __name__ == '__main__':
    # Get user inputs
    parser = argparse.ArgumentParser(
        description='A program to simulate number of battles required to complete the World of Warships Ranked Season.'
    )
    parser.add_argument(
        '-w',
        '--win-rate',
        metavar='win-rate',
        type=float,
        default=DEFAULT_WIN_RATE,
        help='Chance of a player winning a game (enter as a decimal). For example a 55%% win rate is 0.55. Default: %(default).2f'
    )
    parser.add_argument(
        '-f',
        '--first-rate',
        metavar='first-rate',
        type=float,
        default=DEFAULT_FIRST_RATE,
        help='Chance of a player getting first place (enter as a decimal). For example a 10%% first place rate is 0.1. Default: %(default).2f'
    )
    parser.add_argument(
        '-m',
        '--max-battles',
        metavar='max-battles',
        type=int,
        default=DEFAULT_MAX_BATTLES,
        help='Maximum number of battles in a single simulation. Default: %(default)d'
    )
    parser.add_argument(
        '-s',
        '--simulations',
        metavar='simulations',
        type=int,
        default=DEFAULT_SIMULATION_RUNS,
        help='Number of simulations to run. Default: %(default)d'
    )
    args = parser.parse_args()

    # Run simulation
    results = [one_run(args.win_rate, args.first_rate, max_battles=args.max_battles) for _ in range(args.simulations)]
    # TODO: Add histogram bin for ">max battles limit"

    # Create histogram bins/data
    data = Counter(results)
    count = sum(data.values())
    x = list(range(max(data.keys()) + 1))  # This ensures that all bins from 0 to max battles are created
    y = [100 * data[key] / count for key in x]  # convert to prob density function (%)

    # Draw figure
    fig = plt.figure()
    fig.suptitle(f'Battles needed to reach Rank {end_rank} starting from Rank {start_rank}:')
    plt.title(f'Assumes {args.win_rate:.0%} win rate and {args.first_rate:.0%} chance of keeping star after a loss.')
    plt.bar(x, y, align='edge')  # TODO: support multiple plots?
    plt.xlabel('Required Battles')
    plt.ylabel('Percent Chance')
    plt.savefig(f'wows-ranked-simulation-{args.win_rate * 100:.0f}wr-{args.first_rate * 100:.0f}fr.png', dpi=300)
