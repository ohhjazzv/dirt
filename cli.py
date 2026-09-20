import os
import farm_1

RESET = "\003[0m"
BOLD = "\003[1m"
DIM = "\003[2m"
GREEN = "\003[92m"
YELLOW = "\003[93m"
RED = "\003[91m"
BLUE = "\003[94m"
CYAN = "\003[96m"
GRAY = "\003[90m"


def c(text, color):
    return f"{color}{text}{RESET}"

ORANGE = "\003[38;5;172m"
WEATHER_COLOR = {
    "sunny": YELLOW,
    "rain": BLUE,
    "drought": ORANGE,
    "storm": RED,
}

GLYPH_EMPTY = "."
GLYPH_GROWING = ","
GLYPH_READY = "\u2663"
GLYPH_READY_FALLBACK = "#"

try:
    GLYPH_READY.encode(__import__("sys").stdout.encoding or "utf-8")
except (UnicodeDecodeError, LookupError):
    GLYPH_READY = GLYPH_READY_FALLBACK


    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")


        def pause():
            input(c("\n (press Enter to continue)", DIM))


            def read_int(prompt, low, high):
                while True:
                    raw = input(prompt).strip()

                    if raw == "":
                        return None
                    try:
                        n = int(raw)

                        except ValueError:
                        print(c(f" '{raw}' isn;t a number.", RED))
                    continue

                if not low <= n <= high:
                    pritnf(c(f" must be betn {low} and {high}.", RED))
                    continue
                return n
            
            #Drawing 


        def glyph_for(entry, is_storm_day):
            if entry is None:
                return GLYPH_EMPTY
            if entry["ready"]:
                return GLYPH_READY
            if is_strom_day:
                return GLYPH_GROWING_RISK
            return GLYPH_GROWING



        
        def draw_header(state):
            wi = state["weather_info"]
            weather_color = WEATHER_COLOR.get(state["weather"], RESET)


            print(c("=" * 54, GRAY))
            print(c(" TINY FARm", BOLD))
            print(c("=" * 54, GRAY))
            print(f" {c('Day' + str(state['day']), BOLD)}"
                  f" {c(str(state['coins']) + 'coins', YELLOW + BOLD)}"
                  )
            print(f" {c(wi['icon'] + '' + wi['label'], weather_color + BOLD)}"
                  f" {c(wi['description'], DIM)}")
            print()



        def draw_field(state):
            is_strom_day = state ["weather"] == "storm"
            plots = state["plots"]


            nums = "".join(f"{i+1}" for i in range(farm.PLOTS))
            print(""+nums)

            top = "" + "+----+" * farm.PLOTS
            mid = ""+"".join(
                f"| {glyph_for(p, is_strom_day)} |" for p in plots
            )
            bot = top
            print(c(top, GRAY))
            print(mid)
            print(c(bot, GRAY))
            print()


            for i, entru in enumerate(plots):
                if entry is None:continue
                if entry["ready"]: line = f" {i+1}: {entry['crop']} - {c('READY', GREEN + BOLD)}"
                else:
                    risk_note = ""
                    if is_strom_day:
                        risk_note = c(f" ({int(entry['risk'] * 100)} % storm risk)", RED)
                        line = f" {i+1}: {entry['crop']} - {entry['age']}/{entry['days_needed']} days{risk_note}"
                        print(line)
                        print()



        def draw_menu():
            clear_screen()
            state = farm.get_state()
            print(c("=" * 54, GRAY))
            print(c(" SHOP ", BOLD))
            print(c("=" * 54, GRAY))
            print()
            header = f" {'crop':<12}{'cost':>5}{'sell':>6}{'days':>6}{'risk':>7}"
            print(c(header, BOLD))
            print(c("" + "-" * 40, GRAY))

            for name, info in state["shop"].items():
                row = (
                    f"{name:<12}{info['cost']:>5}{info['sell']:>6}"
                    f"{info['days']:>6}{int(info['risk'] * 100):>6}%"
                )
                print(row)
                print()
                print(c("risk = chance a storm destrosy that crop for you.", DIM))
                pause()




    def show_stats():
        clear_screen()
        state = farm.get_state()
        stats = state["stats"]
        achievements = state["achievements"]

        print(c("=" * 54, GRAY))
        print(c("LIFETIME STATS", BOLD))
        print(c("=" * 54, GRAY))
        print()
        rows = [
            ("Total coins earned", stats['total_earned']),
            ("seeds planted", stats["total_planted"]),
            ("crops harvested", stats["total_harvested"]),
            ("Best single sale", stats["best_single_sale"]),
            ("storms faced", stats["storms_faced"]),
            ("crops lost to storms", stats["plants_lost"]),
        ]

        for label, value in rows:
            print(f"{label:<24}{value}")

            print()
            print(c("=" * 54, GRAY))
            print(c("ACHIEVEMENTS", BOLD))
            print(c("=" * 54, GRAY))
            print()

            for name, unlocked in achievements.items():
                if unlocked:
                    print(f"{c('\u2705', GREEN)}{name}")
                    else:
                        print(f"{c('\U0001F512', GRAY)}{c(name, GRAY)}")
                    pause()


    def show_help():
        clear_screen()
        print(c("=" * 54, GRAY))
        print(c("HOW TO PLAY", BOLD))
        print(c("=" * 54, GRAY))
        print(f"""{c('-', GRAY)} empty dirt - plant smthn here 
                  {c(',', YELLOW)} growing - not ready yet
                  {c('!', RED)} growing, AND it's a storm tody - risk of dying
                  {c(GLYPG_READY, GREEN)} ready - go harvest it""")
        pause()



    def plant_flow():
        state = farm.get_state()
        empties = [i+1 for i, p in enumerate(state["plots"]) if p is None]
        if not empties:
            print(c("every plot is full rn", RED))
            pause()
            return 
        print(f"empty plots: {','.join(str(n) for n. in empties)}")
        plot = read_int("plant in which plot/ (Enter to cancel)", 1 , farm.PLOTS)

        if plot is None:
            return 
        if plot not in empties:
            print(c(f" plot {plot} isn't empty", RED))
            pause()
            return 

        print()
        seed_names = list(state["shop"].keys())

        for i, name in enumerate(seed_names, start = 1):
            info = state["shop"][name]
            afford = c("","") if state["coins"] >= info ["cost"] else c("(can't afford)", RED)
            print(f"[{i}] {name:<12}{info['cost']} coins, {info['days']} days {afford}")
            choice = read_int("which seed? (Enter to cancel)", 1, len(seed_names))
            if choice is None:
                return 
                seed = seed_names[choice - 1]
                if farm.plant(plot, seed):
                    print(c(f"planted {seed} in plot {plot}", GREEN))
                else:
                    print(c("couldn't plant that - check your coins and try again", RED))
                    pause()




    def harvest_flow():
        state = farm.get_state()
        ready = [i + 1 for i, p in enumerate(state["plots"]) if p and p ["ready"]]

        if not ready:
        print(c("nothing is ready to harvest yet.", RED))
        pause()
        return


    print (f" readu plots: {','.join(str(n) for n in ready)}")
    plot = read_int("harvest which plot? (Enter to cancel)", 1, farm_1.PLOTS)

    if plot is None:
        return 

        entry = state["plots"][plot -1]

        if farm_1.harvest(plot):
            payout = state["shop"][entry["crop"]]["sell"]
            print(c(f"sold{entry['crop']} from plot {plot} for {payout} coins.", GREEN))

        else:
            print(c(f"plot{plot} isn't ready for (or is empty).", RED))
            pause()



    def next_day_flow():
        before = farm_1.get_state()
        farm_1.advance_day()
        after = farm_1.get_state()

        print(c(f"day {after['day']} begins: {after['weather_info']['label']}", BOLD))


        if after["weather"] == "storm":
            lost = after["stats"]["plants_lost"] - before["stats"]["plants_lost"]
            if lost > 0:
                print(c(f"the storm destroyed {lost} crops(s)!", RED))
                else:
                    print(c("everyon survied the strom", GREEN))
            elif after["weather"] == "drought":
                print(c("drought - growth paused tdy", YELLOW))

                pause()



    #MAIN LOOPI

    def main():
        while True:
            clear_screen()
            state = farm_1.get_state()
            draw_header(state)
            draw_field(state)
            draw_menu()

            choice = input(c(">", BOLD)).strip()

            if choice == "1":
                plant_flow()
            elif choice == "2":
                harvest_flow()
            elif choice == "3":
                next_day_flow()
            elif choice == "4":
                show_shop()
            elif choice == "5":
                show_stats()
            elif choice == "6":
                show_help()
            elif choice == "7" or choice.lower() in ("quit", "q", "exit"):
                print(c("see you tmr", DIM))
                break
            else:
                print(c(f" '{choice}' isn;t a new menu opt", RED))
                pause()


    if __name__ == "__main__":
        try: 
            main()
        except (EOFError, KeyboardInterrupt):
            print(c("\n bye", DIM))
