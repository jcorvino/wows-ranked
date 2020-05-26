import random
from collections import Counter
import matplotlib.pyplot as plt

# Configuration
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
# end_rank = min(ranks.keys())
end_rank = 17


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
                stars = ranks[simulated_rank]['stars'] - 1

        if battles > max_battles:
            break

    return battles


if __name__ == '__main__':
    # TODO: Add user args

    results = [one_run(DEFAULT_WIN_RATE, DEFAULT_FIRST_RATE) for _ in range(DEFAULT_SIMULATION_RUNS)]
    # TODO: Add histogram bin for ">max battles limit" so we're not removing valid simulation data.

    # Create histogram bins/data
    data = Counter(results)
    count = sum(data.values())
    x = data.keys()
    y = [100 * data[key] / count for key in x]  # convert to prob density function (%)

    optbins = max(results) - min(results)  # determines bin number for 1:1 bins

    # Draw figure
    fig = plt.figure()
    fig.suptitle(f'Battles needed to reach Rank {end_rank} starting from Rank {start_rank}:')
    plt.title(f'Assumes {DEFAULT_WIN_RATE:.0%} win rate and {DEFAULT_FIRST_RATE:.0%} chance of keeping star after a loss.')
    plt.bar(x, y)  # TODO: support multiple plots?
    plt.xlabel('Required Battles')
    plt.ylabel('Percent Chance')

    plt.savefig('wows-ranked-simulation.png', dpi=300)
