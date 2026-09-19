CROPS = {
    "Wheat": {"cost": 3,  "sell": 8,  "days": 3},
    "Chili": {"cost": 8,  "sell": 22, "days": 5},
    "Melon": {"cost": 20, "sell": 65, "days": 8},
}

coins = 10
day = 1
plots = [None] * 6


def plant(plot, seed):
    global coins
    idx = plot - 1
    if plots[idx] is not None:
        return {"ok": False, "message": "plot " + str(plot) + " is already planted"}
    cost = CROPS[seed]["cost"]
    if coins < cost:
        return {"ok": False, "message": "need " + str(cost) + " coins, have " + str(coins)}
    coins = coins - cost
    plots[idx] = {"crop": seed, "age": 0, "days_needed": CROPS[seed]["days"], "ready": False}
    return {"ok": True, "message": "planted " + seed + " in plot " + str(plot)}


def harvest(plot):
    global coins
    idx = plot - 1
    entry = plots[idx]
    if entry is None:
        return {"ok": False, "message": "plot " + str(plot) + " is empty"}
    if not entry["ready"]:
        left = entry["days_needed"] - entry["age"]
        return {"ok": False, "message": "needs " + str(left) + " more days"}
    payout = CROPS[entry["crop"]]["sell"]
    coins = coins + payout
    plots[idx] = None
    return {"ok": True, "message": "sold " + entry["crop"] + " for " + str(payout)}


def advance_day():
    global day
    day = day + 1
    for entry in plots:
        if entry is not None:
            entry["age"] = entry["age"] + 1
            entry["ready"] = entry["age"] >= entry["days_needed"]
    return {"ok": True, "message": "day " + str(day) + ", weather: sunny"}


def get_state():
    return {"day": day, "coins": coins, "weather": "sunny", "plots": plots}