import os

import farm_1 as farm


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def symbol_for(plot):
    if plot is None:
        return " .  "
    elif plot["ready"]:
        return plot["crop"][0].upper() + "!  "
    else:
        left = plot["days_needed"] - plot["age"]
        return plot["crop"][0].lower() + str(left) + "  "


def bar_for(plot):
    if plot is None:
        return "          "
    width = 8
    filled = int(plot["age"] / plot["days_needed"] * width)
    if filled > width:
        filled = width
    empty = width - filled
    return "[" + ("#" * filled) + (" " * empty) + "]"


def draw_field(state):
    plots = state["plots"]
    for row in range(2):
        top = ""
        bottom = ""
        for col in range(3):
            i = row * 3 + col
            top = top + "  [" + str(i + 1) + "] " + symbol_for(plots[i])
            bottom = bottom + "      " + bar_for(plots[i]) + " "
        print(top)
        print(bottom)
        print("")


def ask_for_plot():
    plot_text = input("which plot (1-6)? ")

    if not plot_text.isdigit():
        print("that's not a number gng")
        return None

    plot_number = int(plot_text)

    if plot_number < 1 or plot_number > 6:
        print("plot must be 1 to 6")
        return None

    return plot_number


def do_shop():
    print("")
    print("seeds you can plant:")
    for name in farm.SHOP:
        crop = farm.SHOP[name]
        print(" ", name, "- costs", crop["cost"], "- sells for", crop["sell"], "- takes", crop["days"], "days")
    input("press enter ")


def do_plant(state):
    plot_number = ask_for_plot()
    if plot_number is None:
        return

    names = list(farm.SHOP)

    print("")
    for n in range(len(names)):
        crop = farm.SHOP[names[n]]
        print(" ", n + 1, ")", names[n], "-", crop["cost"], "coins")

    seed_text = input("which seed? ")

    if not seed_text.isdigit():
        print("that's not a number gng")
        return

    seed_number = int(seed_text)

    if seed_number < 1 or seed_number > len(names):
        print("pick 1 to " + str(len(names)))
        return

    seed = names[seed_number - 1]

    result = farm.plant(plot_number, seed)
    print(result["message"])
    input("press enter ")


def do_harvest(state):
    plot_number = ask_for_plot()
    if plot_number is None:
        return

    result = farm.harvest(plot_number)
    print(result["message"])
    input("press enter ")


while True:
    clear()
    state = farm.get_state()
    print("")
    print("Day", state["day"], "· Coins:", state["coins"], "·", state["weather"])
    print("")
    draw_field(state)
    print("1) plant  2) harvest  3) shop  4) next day  5) quit")
    choice = input("> ")

    if choice == "5":
        print("bye")
        break
    elif choice == "":
        pass
    elif choice == "1":
        do_plant(state)
    elif choice == "2":
        do_harvest(state)
    elif choice == "3":
        do_shop()
    elif choice == "4":
        result = farm.advance_day()
        print(result["message"])
        input("press enter ")
    else:
        print("not built yet")