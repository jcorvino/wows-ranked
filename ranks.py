# Season 16 rank information
# Assumes rank 18-11 give a free star same as season 15 https://worldofwarships.com/en/news/general-news/ranked-15/
# TODO: Fix rank 17 logic since stars can't be lost (see https://worldofwarships.com/en/news/general-news/ranked-15/).
regular_ranks = {
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
        'free-star': False
    },
    9: {
        'stars': 4,
        'irrevocable': False,
        'free-star': False
    },
    8: {
        'stars': 4,
        'irrevocable': False,
        'free-star': False
    },
    7: {
        'stars': 4,
        'irrevocable': False,
        'free-star': False
    },
    6: {
        'stars': 4,
        'irrevocable': False,
        'free-star': False
    },
    5: {
        'stars': 5,
        'irrevocable': False,
        'free-star': False
    },
    4: {
        'stars': 5,
        'irrevocable': False,
        'free-star': False
    },
    3: {
        'stars': 5,
        'irrevocable': False,
        'free-star': False
    },
    2: {
        'stars': 5,
        'irrevocable': False,
        'free-star': False
    },
    1: {
        'stars': 1,
        'irrevocable': True,
        'free-star': True
    }
}

# Ranked sprint. Based on season 5.
# See https://worldofwarships.com/en/news/general-news/ranked-sprint-5/
sprint_ranks = {
    10: {
        'stars': 1,
        'irrevocable': True,
        'free-star': False
    },
    9: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    8: {
        'stars': 2,
        'irrevocable': True,
        'free-star': True
    },
    7: {
        'stars': 2,
        'irrevocable': False,
        'free-star': True
    },
    6: {
        'stars': 2,
        'irrevocable': False,
        'free-star': True
    },
    5: {
        'stars': 3,
        'irrevocable': True,
        'free-star': True
    },
    4: {
        'stars': 3,
        'irrevocable': False,
        'free-star': True
    },
    3: {
        'stars': 3,
        'irrevocable': True,
        'free-star': True
    },
    2: {
        'stars': 3,
        'irrevocable': False,
        'free-star': True
    },
    1: {
        'stars': 1,
        'irrevocable': True,
        'free-star': True
    }
}
