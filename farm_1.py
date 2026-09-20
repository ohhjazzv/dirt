import json
import os
import random

_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_data.json")
PLOTS = 6
START_COINS = 10

SHOP = {
    "Wheat": {"cost": 3, "sell": 8, "days": 3, "risk": 0.05},
    "Chili": {"cost": 8, "sell": 22, "days": 5, "risk": 0.10},
    "Melon": {"cost": 20, "sell": 65, "days": 8, "risk": 0.15},
}

WEATHER_CHOICES = ["sunny", "rain", "storm"]
WEATHER_WEIGHTS = [0.6, 0.3, 0.1]

_state = None


def _fresh_state():
    return {
        "day": 1,
        "coins": START_COINS,
        "weather": "sunny",
        "plots": [None] * PLOTS,
        "stats": {
            "total_earned": 0,
            "total_planted": 0,
            "total_harvested": 0,
            "best_single_sale": 0,
            "storms_faced": 0,
            "plants_lost": 0,
        },
    }


def _load():
    global _state
    if _state is not None:
        return
    if os.path.exists(_SAVE_PATH):
        try:
            with open(_SAVE_PATH, "r") as f:
                _state = json.load(f)
            if "plots" not in _state or len(_state["plots"]) != PLOTS:
                _state = _fresh_state()
        except (json.JSONDecodeError, OSError):
            _state = _fresh_state()
    else:
        _state = _fresh_state()

    if "stats" not in _state:
        _state["stats"] = _fresh_state()["stats"]


def _save():
    with open(_SAVE_PATH, "w") as f:
        json.dump(_state, f, indent=2)


def _plot_index(plot):
    """1-based -> 0-based, or None if out of range."""
    if not isinstance(plot, int) or not 1 <= plot <= PLOTS:
        return None
    return plot - 1


def _is_ready(entry):
    return entry is not None and entry["age"] >= entry["days_needed"]


def _compute_achievements():
    s = _state["stats"]
    return {
        "First Harvest": s["total_harvested"] >= 1,
        "Green Thumb": s["total_planted"] >= 10,
        "High Roller": s["best_single_sale"] >= 65,
        "Farm Tycoon": s["total_earned"] >= 500,
        "Storm Survivor": s["storms_faced"] >= 5,
        "Untouchable": s["storms_faced"] >= 3 and s["plants_lost"] == 0,
        "Century Farmer": _state["day"] >= 100,
    }


def plant(plot, seed):
    _load()
    idx = _plot_index(plot)
    if idx is None:
        return {"ok": False, "message": f"plot must be 1-{PLOTS}."}
    if seed not in SHOP:
        return {"ok": False, "message": f"no such seed: {seed}"}
    if _state["plots"][idx] is not None:
        return {"ok": False, "message": f"plot {plot} is already planted."}

    cost = SHOP[seed]["cost"]
    if _state["coins"] < cost:
        return {"ok": False, "message": f"need {cost} coins, have {_state['coins']}."}

    _state["coins"] -= cost
    _state["plots"][idx] = {
        "crop": seed,
        "age": 0,
        "days_needed": SHOP[seed]["days"],
        "ready": False,
    }
    _state["stats"]["total_planted"] += 1
    _save()
    return {"ok": True, "message": f"planted {seed} in plot {plot}."}


def harvest(plot):
    _load()
    idx = _plot_index(plot)
    if idx is None:
        return {"ok": False, "message": f"plot must be 1-{PLOTS}."}
    entry = _state["plots"][idx]
    if entry is None:
        return {"ok": False, "message": f"plot {plot} is empty"}
    if not _is_ready(entry):
        left = entry["days_needed"] - entry["age"]
        return {"ok": False, "message": f"plot {plot} needs {left} more day(s)."}

    payout = SHOP[entry["crop"]]["sell"]
    _state["coins"] += payout
    _state["plots"][idx] = None

    _state["stats"]["total_earned"] += payout
    _state["stats"]["total_harvested"] += 1
    if payout > _state["stats"]["best_single_sale"]:
        _state["stats"]["best_single_sale"] = payout

    _save()
    return {"ok": True, "message": f"sold {entry['crop']} from plot {plot} for {payout}."}


def advance_day():
    _load()
    events = []

    weather = random.choices(WEATHER_CHOICES, weights=WEATHER_WEIGHTS, k=1)[0]
    _state["weather"] = weather

    if weather == "storm":
        _state["stats"]["storms_faced"] += 1

    for i, entry in enumerate(_state["plots"]):
        if entry is None:
            continue
        if weather == "storm":
            risk = SHOP[entry["crop"]]["risk"]
            if random.random() < risk:
                events.append(f"storm destroyed the {entry['crop']} in plot {i + 1}.")
                _state["plots"][i] = None
                _state["stats"]["plants_lost"] += 1
                continue
        entry["age"] += 1
        entry["ready"] = entry["age"] >= entry["days_needed"]

    _state["day"] += 1
    _save()

    message = f"day {_state['day']}, weather: {weather}."
    if events:
        message += " " + " ".join(events)
    return {"ok": True, "message": message, "events": events}


def get_state():
    _load()
    return {
        "day": _state["day"],
        "coins": _state["coins"],
        "weather": _state["weather"],
        "plots": [None if p is None else dict(p) for p in _state["plots"]],
        "shop": {k: dict(v) for k, v in SHOP.items()},
        "stats": dict(_state["stats"]),
        "achievements": _compute_achievements(),
    }