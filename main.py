import fakefarm as farm


def symbol_for(plot):
    if plot is None:
        return "."
    elif plot["ready"]:
        return "♣"
    else:
        return ","


def draw_field(state):
    plots = state["plots"]
    for row in range(2):
        line = ""
        for col in range(3):
            i = row * 3 + col
            line = line + "  [" + str(i + 1) + "] " + symbol_for(plots[i])
        print(line)


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
    for name in farm.CROPS:
        crop = farm.CROPS[name]
        print(" ", name, "- costs", crop["cost"], "- sells for", crop["sell"], "- takes", crop["days"], "days")


def do_plant(state):
    plot_number = ask_for_plot()
    if plot_number is None:
        return

    names = list(farm.CROPS)

    print("")
    for n in range(len(names)):
        crop = farm.CROPS[names[n]]
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


def do_harvest(state):
    plot_number = ask_for_plot()
    if plot_number is None:
        return

    result = farm.harvest(plot_number)
    print(result["message"])


while True:
    state = farm.get_state()
    print("")
    print("Day", state["day"], "· Coins:", state["coins"], "·", state["weather"])
    draw_field(state)
    print("")
    print("1) plant  2) harvest  3) shop  4) next day  5) quit")
    choice = input("> ")

    if choice == "5":
        print("bye")
        break
    elif choice == "1":
        do_plant(state)
    elif choice == "2":
        do_harvest(state)
    elif choice == "3":
        do_shop()
    elif choice == "4":
        result = farm.advance_day()
        print(result["message"])
    else:
        print("not built yet")
        