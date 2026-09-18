"""
farm.py — all data + rules. ZERO prints, zero input().

4 functions, that's the whole interface:
    plant(plot, seed)   -> True if it worked, False if any check failed
    harvest(plot)       -> FAKE for now, not wired up yet
    advance_day()        -> FAKE for now, not wired up yet
    get_state()          -> dict of real day/coins/plots

`plot` is 1-based (1..6) in plant()/harvest(), matching the on-screen labels.
"""

# --- crop definitions: what you can plant, what it costs, what it needs ---
SHOP = {
    "wheat": {"cost": 3,  "sell": 8,  "days": 3},
    "chili": {"cost": 8,  "sell": 22, "days": 5},
    "melon": {"cost": 20, "sell": 65, "days": 8},
}

PLOTS = 6

# --- real state, no more fake numbers ---
plots = [None] * PLOTS   # 6 empty plots
coins = 50
day = 1


def plant(plot, seed):
    global coins

    # 1. plot number valid?
    if not isinstance(plot, int) or plot < 1 or plot > PLOTS:
        return False
    idx = plot - 1

    # 2. plot empty?
    if plots[idx] is not None:
        return False

    # 3. seed exists?
    if seed not in SHOP:
        return False

    # 4. enough coins?
    cost = SHOP[seed]["cost"]
    if coins < cost:
        return False

    # all four checks passed — do it
    coins -= cost
    plots[idx] = {"crop": seed, "age": 0}
    return True


def harvest(plot):
    global coins

    # 1. plot number valid?
    if not isinstance(plot, int) or plot < 1 or plot > PLOTS:
        return False
    idx = plot - 1

    entry = plots[idx]
    # 2. is there anything there?
    if entry is None:
        return False

    # 3. is it actually ready?
    needed = SHOP[entry["crop"]]["days"]
    if entry["age"] < needed:
        return False

    # sell it, clear the plot
    coins += SHOP[entry["crop"]]["sell"]
    plots[idx] = None
    return True


def advance_day():
    global day
    for entry in plots:
        if entry is not None:
            entry["age"] += 1
    day += 1
    return True


def get_state():
    state_plots = []
    for entry in plots:
        if entry is None:
            state_plots.append(None)
            continue
        needed = SHOP[entry["crop"]]["days"]
        state_plots.append({
            "crop": entry["crop"],
            "age": entry["age"],
            "days_needed": needed,
            "ready": entry["age"] >= needed,
        })

    return {
        "day": day,
        "coins": coins,
        "plots": state_plots,
        "shop": {k: dict(v) for k, v in SHOP.items()},
    }
