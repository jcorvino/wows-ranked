import random
import argparse
import multiprocessing as mp
from collections import Counter
from typing import Callable, List
import statistics
from pathlib import Path, PurePath
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from ranks import regular_ranks, sprint_ranks


# Defaults
DEFAULT_FIRST_RATE = 1 / 7  # chance to get 1st place in a battle
# DEFAULT_WIN_RATE = 0.5  # chance to win a battle
DEFAULT_MAX_BATTLES = 10000  # maximum number of battles before simulation stops
DEFAULT_SIMULATION_RUNS = 50000  # number of times to run the simulation
DEFAULT_WIN_RATE_LIST = [x/100 for x in range(48, 101)]  # win rates to simulate


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


def parallel_runs(func: Callable, func_args: tuple, num_runs: int) -> List:
    """
    Run a function in parallel. Uses the same inputs for each function call.

    :param func: Function to run
    :param func_args: Arguments to that function (will be identical for all runs)
    :param num_runs: number of function calls (aka runs)
    :return: list of function outputs
    """
    pool_size = mp.cpu_count()
    output = []
    with mp.Pool(processes=pool_size) as pool:
        pool.starmap_async(
            func,
            [func_args] * num_runs,
            callback=output.extend
        )
        pool.close()
        pool.join()
    return output


# TODO: Cleanup user args and match them with the README.md
def parse_user_args() -> argparse.Namespace:
    """
    Get user inputs

    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='A program to simulate number of battles required to complete the World of Warships Ranked Season.'
    )
    parser.add_argument(
        '-w',
        '--win-rates',
        metavar='win-rates',
        nargs='+',
        type=float,
        default=DEFAULT_WIN_RATE_LIST,
        help='Chances of a player winning a game that you want to simulate (enter as space separated decimals). \
            For example if you want to simulate a 55%% and 60%% win rate, enter "0.55 0.60". Default: %(default)s'
    )
    parser.add_argument(
        '-f',
        '--first-rate',
        metavar='first-rate',
        type=float,
        default=DEFAULT_FIRST_RATE,
        help='Chance of a player getting first place (enter as a decimal). \
            For example a 10%% first place rate is 0.1. Default: %(default).2f'
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
        help='Number of simulations to run for a single win rate. Default: %(default)d'
    )
    parser.add_argument(
        '-o',
        '--output-folder',
        metavar='output-folder',
        type=str,
        default='output',
        help='Name of output folder. Default: %(default)s'
    )
    parser.add_argument(
        '--sprint',
        action='store_true',
        help='Use this flag to simulate ranked sprint season. \
            By default the program will simulate a normal ranked season.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    # Get user inputs
    args = parse_user_args()

    # Create output folder if needed
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)

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

    summary_data = {}
    for wr in args.win_rates:
        # Run simulation in parallel for each win rate
        print(f'Simulating win rate {wr}')
        one_run_inputs = (wr, args.first_rate, ranks, start_rank, end_rank, args.max_battles)
        output_list = parallel_runs(one_run, one_run_inputs, args.simulations)

        # Get median and mean
        median = statistics.median(output_list)
        mean = statistics.mean(output_list)

        # Save data for summary analysis
        output_dict = {
            'raw-output': output_list,
            'median': median,
            'mean': mean

        }
        summary_data[wr] = output_dict

        # Create histogram bins/data
        # TODO: Add histogram bin for ">max battles limit"
        data = Counter(output_list)
        count = sum(data.values())
        x = list(range(max(data.keys()) + 1))  # This ensures that all bins from 0 to max battles are created
        y = [100 * data[key] / count for key in x]  # convert to prob density function (%)

        # Draw figure
        fig = plt.figure()
        fig.suptitle(f'Battles needed to reach rank {end_rank} starting from rank {start_rank} ({rank_type} season):')

        # Add data
        plt.bar(x, y, align='edge', width=1)
        plt.axvline(median, color='r', linestyle='dashed', linewidth=1, label=f'Median = {int(median)}')
        plt.axvline(mean, color='k', linestyle='dashed', linewidth=1, label=f'Mean = {mean:.1f}')

        # Add labels
        plt.legend(loc='upper left')
        plt.title(f'Assumes {wr:.0%} win rate and {args.first_rate:.0%} chance of keeping star after a loss.')
        plt.xlabel('Required Battles')
        plt.ylabel('Percent Chance')

        # Save figure
        filename = PurePath(
            args.output_folder,
            f'wows-ranked-{rank_type}-simulation-{wr * 100:.0f}wr-{args.first_rate * 100:.0f}fr.png'
        )
        plt.savefig(filename, dpi=800)
        plt.close(fig)  # close so we don't consume too much memory

    # Create summary plot
    x = [k * 100 for k in summary_data.keys()]
    y = [val['median'] for val in summary_data.values()]

    # Draw figure
    fig = plt.figure()
    fig.suptitle(f'Battles needed to reach rank {end_rank} starting from rank {start_rank} ({rank_type} season):')

    # Add data
    plt.plot(x, y)

    # Add labels
    plt.title(f'Assumes {args.first_rate:.0%} chance of keeping star after a loss.')
    plt.xlabel('Win Rate')
    plt.ylabel('Median Battles Required')

    # Ajust axis
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xlim([None, 100])
    ax.set_ylim([0, None])

    # Save figure
    filename = PurePath(
        args.output_folder,
        f'wows-ranked-{rank_type}-summary-{args.first_rate * 100:.0f}fr.png'
    )
    plt.savefig(filename, dpi=800)
    plt.close(fig)  # close so we don't consume too much memory
