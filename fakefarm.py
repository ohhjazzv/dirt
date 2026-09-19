CROPS = {
    "wheat":  {"days": 3, "cost": 5,  "sells": 12},
    "carrot": {"days": 5, "cost": 10, "sells": 30},
}


def plant(plot_index, seed_name):
    return True


def harvest(plot_index):
    return 0


def advance_day():
    pass


def get_state():
    return {"day": 1, "coins": 50, "plots": [None] * 6}