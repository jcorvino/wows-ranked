import random
import argparse
import multiprocessing as mp
from collections import Counter
import matplotlib.pyplot as plt

from ranks import regular_ranks, sprint_ranks


# Defaults
DEFAULT_FIRST_RATE = 1 / 7  # chance to get 1st place in a battle
DEFAULT_WIN_RATE = 0.5  # chance to win a battle
DEFAULT_MAX_BATTLES = 10000  # maximum number of battles before simulation stops
DEFAULT_SIMULATION_RUNS = 50000  # number of times to run the simulation


def one_run(wr: float, fr: float, ranks: dict, start_rank: int, end_rank: int,
            max_battles: int) -> int:
    """
    Simulate battles required to complete ranked season.

    :param wr: win rate
    :param fr: first place rate
    :param ranks: information on stars in each rank
    :param start_rank: initial rank for the simulation
    :param end_rank: final rank (simulation ends when reaching this rank)
    :param max_battles: maximum battles before simulation ends (prevents infinite loops).
    :return: number of battles
    """
    battles = 0
    stars = 0
    simulated_rank = start_rank

    while simulated_rank != end_rank:
        battles += 1
        if battles > max_battles:
            break

        # Determine battle outcome
        if random.random() < wr:
            stars += 1  # win
        elif random.random() >= fr:  # best player doesn't lose star
            stars -= 1  # loss and no star saved

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
    parser.add_argument(
        '-o',
        '--outfile',
        metavar='outfile',
        type=str,
        default=None,
        help='Name of output file.'
    )
    parser.add_argument(
        '--sprint',
        action='store_true',
        help='Use this flag to simulate ranked sprint season. \
        By default the program will simulate a normal ranked season.'
    )
    args = parser.parse_args()

    # Get ranked type
    if args.sprint:
        ranks = sprint_ranks
        rank_type = 'sprint'
    else:
        ranks = regular_ranks
        rank_type = 'regular'

    # Get start and stop rank
    start_rank = max(ranks.keys())
    end_rank = min(ranks.keys())

    # Run simulation
    pool_size = mp.cpu_count()
    results = []
    with mp.Pool(processes=pool_size) as pool:
        pool.starmap_async(
            one_run,
            [(args.win_rate, args.first_rate, ranks, start_rank, end_rank, args.max_battles)] * args.simulations,
            callback=results.extend
        )
        pool.close()
        pool.join()

    # Create histogram bins/data
    # TODO: Add histogram bin for ">max battles limit"
    data = Counter(results)
    count = sum(data.values())
    x = list(range(max(data.keys()) + 1))  # This ensures that all bins from 0 to max battles are created
    y = [100 * data[key] / count for key in x]  # convert to prob density function (%)

    # Draw figure
    fig = plt.figure()
    fig.suptitle(f'Battles needed to reach rank {end_rank} starting from rank {start_rank} ({rank_type} season):')
    plt.title(f'Assumes {args.win_rate:.0%} win rate and {args.first_rate:.0%} chance of keeping star after a loss.')
    plt.bar(x, y, align='edge', width=1)  # TODO: support multiple plots?
    plt.xlabel('Required Battles')
    plt.ylabel('Percent Chance')
    if args.outfile is None:
        filename = f'wows-ranked-{rank_type}-simulation-{args.win_rate * 100:.0f}wr-{args.first_rate * 100:.0f}fr.png'
    else:
        filename = args.outfile
    plt.savefig(filename, dpi=800)
