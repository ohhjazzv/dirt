"""
farm.py — all data + rules. ZERO prints, zero input(). Nothing here talks
to a terminal. main.py is the only thing allowed to draw or read input.

Contract: exactly 4 functions. That's the whole interface.

    plant(plot, seed)  -> {"ok": bool, "message": str}
    harvest(plot)      -> {"ok": bool, "message": str}
    advance_day()      -> {"ok": bool, "message": str, "events": [str, ...]}
    get_state()        -> dict, see shape below. READ-ONLY — mutate the
                          game only through the three functions above.

get_state() shape:
{
  "day": 7,
  "coins": 42,
  "weather": "storm",              # today's weather: sunny | rain | storm
  "plots": [                        # always length 6, index 0..5
      None,                         # empty dirt
      {
        "crop": "wheat",
        "age": 2,                   # days since planted
        "days_needed": 3,           # age >= days_needed means ready
        "ready": False
      },
      ...
  ],
  "shop": {                         # crops on offer, for main.py to render
      "wheat": {"cost": 3,  "sell": 8,  "days": 3, "risk": 0.05},
      "chili": {"cost": 8,  "sell": 22, "days": 5, "risk": 0.10},
      "melon": {"cost": 20, "sell": 65, "days": 8, "risk": 0.15},
  }
}

`plot` arguments are 1-based (1..6), matching how you'll label them on screen.
`seed` is a crop name string, must be a key in shop.

Growth is just "age += 1 per day" — main.py decides what letter to draw by
comparing age to days_needed. This file never picks a letter.

Weather: rolled fresh each advance_day(). On a "storm" day, every alive
plant has its crop's `risk` chance of dying (removed, no refund, no sale).
advance_day() returns which plots died in "events" so main.py can tell
the player what happened.

Persistence: state auto-saves to save_data.json next to this file after
every plant/harvest/advance_day call, and auto-loads on first use. No
save/load function needed in the contract — it just happens.
"""

import json
import os
import random

_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_data.json")

PLOTS = 6
START_COINS = 10

SHOP = {
    "wheat": {"cost": 3,  "sell": 8,  "days": 3, "risk": 0.05},
    "chili": {"cost": 8,  "sell": 22, "days": 5, "risk": 0.10},
    "melon": {"cost": 20, "sell": 65, "days": 8, "risk": 0.15},
}

WEATHER_CHOICES = ["sunny", "rain", "storm"]
WEATHER_WEIGHTS = [0.6, 0.3, 0.1]

_state = None  # lazily loaded


def _fresh_state():
    return {
        "day": 1,
        "coins": START_COINS,
        "weather": "sunny",
        "plots": [None] * PLOTS,
    }


def _load():
    global _state
    if _state is not None:
        return
    if os.path.exists(_SAVE_PATH):
        try:
            with open(_SAVE_PATH, "r") as f:
                _state = json.load(f)
            # basic sanity check in case the save file is stale/corrupt
            if "plots" not in _state or len(_state["plots"]) != PLOTS:
                _state = _fresh_state()
        except (json.JSONDecodeError, OSError):
            _state = _fresh_state()
    else:
        _state = _fresh_state()


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


# ----------------------------------------------------------------------
# the 4 functions
# ----------------------------------------------------------------------

def plant(plot, seed):
    _load()
    idx = _plot_index(plot)
    if idx is None:
        return {"ok": False, "message": f"plot must be 1-{PLOTS}."}
    if seed not in SHOP:
        return {"ok": False, "message": f"no such seed: {seed}."}
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
    _save()
    return {"ok": True, "message": f"planted {seed} in plot {plot}."}


def harvest(plot):
    _load()
    idx = _plot_index(plot)
    if idx is None:
        return {"ok": False, "message": f"plot must be 1-{PLOTS}."}
    entry = _state["plots"][idx]
    if entry is None:
        return {"ok": False, "message": f"plot {plot} is empty."}
    if not _is_ready(entry):
        left = entry["days_needed"] - entry["age"]
        return {"ok": False, "message": f"plot {plot} needs {left} more day(s)."}

    payout = SHOP[entry["crop"]]["sell"]
    _state["coins"] += payout
    _state["plots"][idx] = None
    _save()
    return {"ok": True, "message": f"sold {entry['crop']} from plot {plot} for {payout}."}


def advance_day():
    _load()
    events = []

    weather = random.choices(WEATHER_CHOICES, weights=WEATHER_WEIGHTS, k=1)[0]
    _state["weather"] = weather

    for i, entry in enumerate(_state["plots"]):
        if entry is None:
            continue

        if weather == "storm":
            risk = SHOP[entry["crop"]]["risk"]
            if random.random() < risk:
                events.append(f"storm destroyed the {entry['crop']} in plot {i + 1}.")
                _state["plots"][i] = None
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
    # return a deep-enough copy so main.py can't mutate our internals by accident
    return {
        "day": _state["day"],
        "coins": _state["coins"],
        "weather": _state["weather"],
        "plots": [None if p is None else dict(p) for p in _state["plots"]],
        "shop": {k: dict(v) for k, v in SHOP.items()},
    }
