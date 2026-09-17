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


def do_plant(state):
    plot_text = input("which plot (1-6)? ")

    if not plot_text.isdigit():
        print("that's not a number gng")
        return

    plot_number = int(plot_text)

    if plot_number < 1 or plot_number > 6:
        print("plot must be 1 to 6")
        return

    seed = input("which seed? ")
    worked = farm.plant(plot_number - 1, seed)

    if worked:
        print("planted", seed)
    else:
        print("could not plant", seed)


while True:
    state = farm.get_state()
    print("")
    print("Day", state["day"], "· Coins:", state["coins"])
    draw_field(state)
    print("")
    print("1) plant  2) harvest  3) shop  4) next day  5) quit")
    choice = input("> ")

    if choice == "5":
        print("bye")
        break
    elif choice == "4":
        farm.advance_day()
        print("a day passes.......")
    elif choice == "1":
        do_plant(state)
    else:
        print("not built yet")