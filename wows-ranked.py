import random
import matplotlib.pyplot as plt

# configuration
DEFAULT_FIRST_RATE = 1 / 7  # chance to get 1st place in a battle
DEFAULT_WIN_RATE = 0.5  # chance to win a battle
DEFAULT_MAX_BATTLES = 10000  # maximum number of battles before simulation stops
TOTAL_STARS = 55
ranks = {  # TODO: Include all ranks. dict should hold data about stars in each rank and if the rank is irrevocable.
}


def one_run(wr=DEFAULT_WIN_RATE, fr=DEFAULT_FIRST_RATE):
    """
    Simulate battles required to reach rank 1 starting from rank 12.

    :param wr: win rate
    :param fr: first place rate
    :return: number of battles
    """
    battles = 0
    stars = 0
    while stars < TOTAL_STARS:
        battles += 1
        if random.random() < wr:
            stars += 1
            if stars % 2 == 0 and stars <= 4:
                stars += 1
            elif stars % 4 == 0 and stars <= 24 and stars > 4:
                 stars += 1
            elif stars % 5 == 0 and stars > 24:
                 stars += 1
        else:
            if random.random() < fr and stars > 0:  # best player doesn't lose star + stars can't go below irrevocable
                stars -= 1

        if battles > DEFAULT_MAX_BATTLES:
            break

    return battles


# create list
s = []
for i in range(2):
    n = one_run()
    # TODO: Add histogram bin for ">max battles limit" so we're not removing valid simulation data.
    if n <= DEFAULT_MAX_BATTLES:  # ignore cases that exceed max battles limit.
        s.append(n)

# draw
s.sort()  # TODO: Find a better way to bin. Sort is too slow.
optbins = s[len(s)-1]-s[0]  # determines bin number for 1:1 bins

fig = plt.figure()
fig.suptitle('Battles needed to reach Rank 1 starting from Rank 12:')
plt.title(f'Assumes {DEFAULT_WIN_RATE:.0%} win rate and {DEFAULT_FIRST_RATE:.0%} chance of keeping star after a loss.')
plt.hist(s, bins=optbins, density=True)  # TODO: stop using "density" and create the distribution ourselves.
plt.xlabel('Required Battles')
plt.ylabel('Percent')

plt.savefig('wows-ranked-simulation.png', dpi=300)
