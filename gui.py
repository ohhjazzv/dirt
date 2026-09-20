import tkinter as tk
from tkinter import ttk, messagebox

import farm_1 


BG_MAIN  = "#f4f1ea"
BG_PANEL = "#fffaf0"
BG_STATUSBAR = "#3e5c3a"
BG_LOG = "#1c241c"
FG_LOG = "#8bf28b"

COLOR_EMPTY = "#dfd0b8"
COLOR_GROWING = "#e9e28a"
COLOR_STROM_RISK = "#e3b0a3"
COLOR_READY = "#8bc34a"


ICON_EMPTY = ""
ICON_GROWING = "\U0001F331"
ICON_READY = "\U0001F33E"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_HEADER = ("Arial", 13, "bold")
FONT_BODY = ("Arial", 10)
FONT_MONO = ("courier", 10)

PLOT_W, PLOT_H = 150, 150



class FarmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Farm")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_quit)
        self.plot_frames = []
        self.plot_icons = []
        self.plot_labels = []
        self.plot_bars = []
        self.stat_value_labels = {}
        self.achievement_labels = {}
        self._build_splash_screen()




    def _build_splash_screen(self):
        self.splash = tk.Frame(self.root, bg=BG_MAIN, width = 500, height = 420)
        self.splash.pack(fill="both", expand=True)
        self.splash.pack_propagate(False) 


        tk.Label(
            self.splash, text = "\U0001F33E", font = ("Arial", 64), bg=BG_MAIN,).pack(pady=(60,0))
        tk.Label(
            self.splash, text="TIny Farm", font=("Georgia", 28, "bold"),bg=BG_MAIN, fg="#3e5c3a",).pack(pady=(10,4))
        tk.Label(
            self.splash, text="Six plots, one number going up per plant", font=("Arial", 11, "italic"), bg=BG_MAIN, fg = "#7a7060",).pack(pady=(0, 30))

        tk.Button(
            self.splash, text="Play", font=("Arial", 13, "bold"), activebackground="#2f3a2c", activeforeground="white", padx=30, pady=10, bd=0, command=self.start_game,).pack()


    state = farm.get_state()
    if state["day"] > 1 or state["coins"] != farm.START_COINS:
        tk.Label(
            self.splash,
            text = f"continuing from day {state['day']}, {state['coins']} coins",
            font = ("Arial", 9), bg-BG_MAIN, fg="#999999"
        ).pack(pday=(20,0))




def start_game(self):
    self.splash.desotry()
    self._build_menu_bar()
    self._build_title()
    self._build_notebook()
    self.refresh()



def confirm_quit(self):
    if messagebox.askyesno(
        "QUit TINY Farm"
        "Your Progress is saved auto"
        "ANything. QUIT NOW?"
    ):
        self.root.destory()




def _build_menu_bar(self):
    menubar = tk.Menu(self.root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Quit", command=self.confirm_quit)
    menubar.add_cascade(label="File", menu = file_menu)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="HOw to play", command= self.show_help)
    help_menu.add_command(label="About", command = self.show_about)
    help.add_cascade(label="Help", menu=help_menu)
    self.root.config(menu=menubar)



def  _build_title(self):
    title = tk.Label(
        self.root, text ="\U0001F33E Tiny Farm \U0001F33E"
        font = FONT_TITLE, bg=BG_MAIN, fg="#3e5c3a", pady=10,
    ) title.pack(fill="x")




def _build_notebook(self):
    style = ttk.Style()
    style.configure("TNotebook", background = BG_MAIN)
    style.configure("TNotebook.Tab", font = FONT_BODY, padding = (14,6))

    notebook = ttk.Notebook(self.root)
    notebook.pack(fill="both", expand=True, padx=10, pady=(0,10))
    farm_tab = tk.Frame(notebook, bg=BG_MAIN)
    stats_tab = tk.Frame(notebook, bg=BG_MAIN)
    notebook.add(farm_tab, text="Farm")
    notebook.add(stats_tab, text="Stats& Achievements")
    self._build_farm_tab(farm_tab)
    self._build_stats_tab(stats_tab)




    #FARm tab

def _build_farm_tab(self, parent):
    self._build_status_bar(parent)
    self._build_weather_banner(parent)
    body = tk.Frame(parent, bg=BG_MAIN)
    body.pack(fill="both", expand=True)
    self._build_farm_grid(body)
    self._build_shop_panel(body)
    self._build_log(parent)
    self._build_action_buttons(parent)




def _build_status_bar(self, parent):
    bar = tk.Frame(parent, bg=BG_STATUSBAR, pady = 10)
    bar.pack(fill="x")


    self.day_label = tk.Label(
        bar, text="", font=FONT_HEADER, bg=BG_STATUSBAR, fg="#ffd54f"
    )


    self.coins_label = tk.Label(
        bar, text="", font=FONT_HEADER, bg=BG_STATUSBAR, fg="#ffd54f"
    )

    self.coins_label.pack(side="left", padx=20)






def _build_weather_banner(self, parent):
    self.weather_banner = tk.Frame(parent, bg=BG_PANEL, pady=6)
    self.weather_banner.pack(fill="x", pady=(8,4), padx=2)

    self.weather_label = tk.Label(
        self.weather_banner, text="", font=("Arial", 12, "bold"), bg=BG_PANEL, anchor="w"
    )


    self.weather_lavel.pack(side="left", padx=14)

    self.weather_desc_label =  tk.Label(
        self.weather_banner, text="", font=("Arial", 10, "italic"), bg=BG_PANEL, anchor = "w",
    )

    self.weather_desc_label.pack(side="left")


def _build_farm_grid(self, parent):
    grid = tf.Frame(parent, bg=BG_MAIN, padx=10, pady=10)
    grid.pack(side="left")


for i in range(farm_1.PLOTS):
    r, c = divmod(i,3)
    frame = tk.Frame(grid, width = PLOT_W, height=PLOT_H, bd=2, relief="ridge", bg=COLOR_EMPTY) 
    frame.grid(row=r, column=c, padx=8, pady=8)
    frame.grid_propagate(False)

    icon = tk.Label(frame, text ="", font=("Arial", 34), bg= COLOR_EMPTY)
    icon.pack(pady=(12,0))

    label = tk.Label(frame, text="", font=("Arial", 10), bg=COLOR_EMPTY, justify="ceter")
    label.pack()

    bar_canvas.pack(pady=(6,0))


for widget in (frame, icon, label, bar_canvas):
    widget.bind("<Button-1>", lambda e, idx=i: self.on_plot_click(idx))
    self.plot_framers.append(frame)
    self.plot_icons.append(icon)
    self.plot_labels.appends(label)
    self.plot_bars.append(bar_canvas)




def _build_shop_panel(self, parent):
    panel = tk.Frame(parent, bg=BG_PANEL, bd=2, relief="groove", padx=14, pady=14,)
    panel.pack(side="left", fill="y", padx=(0,10), pady=10)

    tk.Label(panel, text="SHOp", font=FONT_HEADER, bg=BG_PANEL).pack(anchor="w", pady=(0, 10))


    header = f"{'crop':<11}{'cost':>5}{'sell':>6}{'days':>6}{'risk':>7}"
    tk.Label(panel, text=header, font=FONT_MONO, bg=BG_PANEL).pack(anchor="w")
    tk.Frame(panel, bg="#c8b89a", height=1).pack(fill="x", pady=4)



    for name, info in farm.SHOP.itmes():
        row = f"{name:<11}{info['cost']:>5}{info['sell']:>6}{info['days']:>6}{int(info['risk']*100):>6}%"
        tk.Label(panel, text=row, font=FONT_MONO, bg=BG_PANEL, anchor="w").pack(anchor="w", pady=1)


        tk.Label(
            panel, 
            text="\nrisk = chance a storm\n destroys that crop. \n\n Click an empty plot \n to plat smth.",
            font=("Arial", 9, "italic"), bg=BG_PANEL, justify="left",
        ).pack(anchor="w", pady=(14,0))



    

def _build_action_buttons(self,parent):
    row = tk.Frame(parent, bg=BG_MAIN)
    row.pack(pady=10)

harvest_all_btn = tk.Button(
            row, text="Harvest All \u2663", font=("Arial", 12, "bold"),
            bg=COLOR_READY, fg="#2c3e1a", activebackground="#79a83f",
            padx=12, pady=8, bd=0,
            command=self.on_harvest_all,
        )

        harvest_all_btn.pack(side="left", padx=(0, 10))

        next_day_btn = tk.Button(
            row, text="Next Day \u2192", font=("Arial", 12, "bold"),
            bg=BG_STATUSBAR, fg="white", activebackground="#2f4a2c",
            activeforeground="white", padx=12, pady=8, bd=0,
            command=self.on_next_day,
        )
        next_day_btn.pack(side="left")


 def _build_stats_tab(self, parent):
        columns = tk.Frame(parent, bg=BG_MAIN)
        columns.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_stats_panel(columns)
        self._build_achievements_panel(columns)

    def _build_stats_panel(self, parent):
        panel = tk.Frame(parent, bg=BG_PANEL, bd=2, relief="groove", padx=16, pady=16)
        panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(panel, text="Lifetime Stats", font=FONT_HEADER, bg=BG_PANEL).pack(
            anchor="w", pady=(0, 12)
        )

        rows = [
            ("total_earned", "Total coins earned"),
            ("total_planted", "Seeds planted"),
            ("total_harvested", "Crops harvested"),
            ("best_single_sale", "Best single sale"),
            ("storms_faced", "Storms faced"),
            ("plants_lost", "Crops lost to storms"),
        ]
        for key, label_text in rows:
            row = tk.Frame(panel, bg=BG_PANEL)
            row.pack(fill="x", pady=4)
            tk.Label(
                row, text=label_text, font=FONT_BODY, bg=BG_PANEL, anchor="w", width=20
            ).pack(side="left")
            value_label = tk.Label(
                row, text="0", font=("Arial", 10, "bold"), bg=BG_PANEL, anchor="e"
            )
            value_label.pack(side="left")
            self.stat_value_labels[key] = value_label



 def _build_achievements_panel(self, parent):
        panel = tk.Frame(parent, bg=BG_PANEL, bd=2, relief="groove", padx=16, pady=16)
        panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        tk.Label(panel, text="Achievements", font=FONT_HEADER, bg=BG_PANEL).pack(
            anchor="w", pady=(0, 12)
        )

        # order matches farm._compute_achievements() but is defined
        # independently here — this file only ever reads names/values
        # out of get_state(), it never assumes farm.py's internals.
        names = [
            "First Harvest", "Green Thumb", "High Roller",
            "Farm Tycoon", "Storm Survivor", "Untouchable", "Century Farmer",
        ]
        for name in names:
            row = tk.Frame(panel, bg=BG_PANEL)
            row.pack(fill="x", pady=3, anchor="w")
            lbl = tk.Label(
                row, text=f"\U0001F512  {name}", font=FONT_BODY, bg=BG_PANEL, anchor="w"
            )
            lbl.pack(anchor="w")
            self.achievement_labels[name] = lbl

    # ---------------------------------------------------------------
    # help / about dialogs
    # ---------------------------------------------------------------

    def show_help(self):
        messagebox.showinfo(
            "How to Play",
            "Click an empty plot to buy and plant a seed.\n"
            "Click a growing plot to see how many days are left.\n"
            "Click a ready (green) plot to harvest and sell it.\n"
            "Press 'Next Day' to move time forward.\n\n"
            "Watch the weather banner — storms can destroy crops, "
            "and droughts pause all growth for the day.\n\n"
            "Your progress saves automatically."
        )

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Tiny Farm\n\nA tiny terminal-turned-graphical farming game.\n"
            "Logic lives in farm.py. This window is just the face."
        )

    # ---------------------------------------------------------------
    # logging
    # ---------------------------------------------------------------

    def say(self, message, kind="info"):
        colors = {"info": FG_LOG, "warn": "#f2c94c", "bad": "#f28b8b"}
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        # color the line we just added
        line_start = self.log.index("end-2l")
        line_end = self.log.index("end-1l")
        tag = f"tag_{kind}"
        self.log.tag_configure(tag, foreground=colors.get(kind, FG_LOG))
        self.log.tag_add(tag, line_start, line_end)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---------------------------------------------------------------
    # redraw everything from get_state() — the only source of truth
    # ---------------------------------------------------------------

    def refresh(self):
        state = farm.get_state()

        self.day_label.config(text=f"Day {state['day']}")
        self.coins_label.config(text=f"\U0001FA99 {state['coins']} coins")

        wi = state["weather_info"]
        self.weather_label.config(text=f"{wi['icon']} {wi['label']}")
        self.weather_desc_label.config(text=wi["description"])

        is_storm_day = state["weather"] == "storm"

        for i, entry in enumerate(state["plots"]):
            frame = self.plot_frames[i]
            icon = self.plot_icons[i]
            label = self.plot_labels[i]
            bar = self.plot_bars[i]

            if entry is None:
                color = COLOR_EMPTY
                icon.config(text=ICON_EMPTY, bg=color)
                label.config(text="empty\nclick to plant", bg=color)
                bar.config(bg=color)
                bar.delete("all")

            elif entry["ready"]:
                color = COLOR_READY
                icon.config(text=ICON_READY, bg=color)
                label.config(text=f"{entry['crop']}\nready! click", bg=color)
                bar.config(bg=color)
                bar.delete("all")
                w = int(bar["width"])
                bar.create_rectangle(0, 0, w, 10, fill="#4a7a2c", outline="")

            else:
                color = COLOR_STORM_RISK if is_storm_day else COLOR_GROWING
                icon.config(text=ICON_GROWING, bg=color)
                extra = f"\n{int(entry['risk']*100)}% storm risk" if is_storm_day else ""
                label.config(
                    text=f"{entry['crop']}\n{entry['age']}/{entry['days_needed']} days{extra}",
                    bg=color,
                )
                bar.config(bg=color)
                bar.delete("all")
                w = int(bar["width"])
                ratio = entry["age"] / entry["days_needed"]
                bar.create_rectangle(0, 0, w, 10, outline="#8a7a5c")
                bar.create_rectangle(0, 0, int(w * ratio), 10, fill="#c9a227", outline="")

            frame.config(bg=color)

        stats = state["stats"]
        for key, value_label in self.stat_value_labels.items():
            value_label.config(text=str(stats[key]))

        for name, unlocked in state["achievements"].items():
            lbl = self.achievement_labels.get(name)
            if lbl is None:
                continue
            if unlocked:
                lbl.config(text=f"\u2705  {name}", fg="#2e7d32")
            else:
                lbl.config(text=f"\U0001F512  {name}", fg="#999999")

    # ---------------------------------------------------------------
    # click / button handlers — these call farm.py and nothing else
    # ---------------------------------------------------------------

    def on_plot_click(self, idx):
        state = farm.get_state()
        entry = state["plots"][idx]
        plot_number = idx + 1

        if entry is None:
            self.open_plant_dialog(plot_number)

        elif entry["ready"]:
            crop = entry["crop"]
            payout = state["shop"][crop]["sell"]
            if farm.harvest(plot_number):
                self.say(f"sold {crop} from plot {plot_number} for {payout} coins.", "info")
            else:
                self.say(f"couldn't harvest plot {plot_number}.", "bad")
            self.refresh()

        else:
            left = entry["days_needed"] - entry["age"]
            messagebox.showinfo(
                "Still growing",
                f"{entry['crop'].title()} in plot {plot_number} needs "
                f"{left} more day(s)."
            )

    def open_plant_dialog(self, plot_number):
        state = farm.get_state()
        coins = state["coins"]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Plant in plot {plot_number}")
        dialog.configure(bg=BG_MAIN)
        dialog.resizable(False, False)

        tk.Label(
            dialog, text=f"Choose a seed for plot {plot_number}",
            font=FONT_HEADER, bg=BG_MAIN,
        ).pack(padx=20, pady=(15, 10))

        for name, info in state["shop"].items():
            afford = coins >= info["cost"]
            text = f"{name.title():<11} {info['cost']:>3} coins   {info['days']} days"
            btn = tk.Button(
                dialog, text=text, font=FONT_MONO, anchor="w",
                state="normal" if afford else "disabled",
                command=lambda n=name: self.do_plant(plot_number, n, dialog),
            )
            btn.pack(fill="x", padx=20, pady=3)

        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=(12, 15))

    def do_plant(self, plot_number, seed, dialog):
        dialog.destroy()
        if farm.plant(plot_number, seed):
            self.say(f"planted {seed} in plot {plot_number}.", "info")
        else:
            messagebox.showwarning(
                "Can't plant that",
                "Either you don't have enough coins, or something else changed."
            )
        self.refresh()

    def on_harvest_all(self):
        state = farm.get_state()
        total_payout = 0
        harvested_count = 0

        for i, entry in enumerate(state["plots"]):
            if entry is not None and entry["ready"]:
                payout = state["shop"][entry["crop"]]["sell"]
                if farm.harvest(i + 1):
                    total_payout += payout
                    harvested_count += 1

        if harvested_count == 0:
            self.say("nothing ready to harvest.", "warn")
        else:
            self.say(
                f"harvested {harvested_count} plot(s) for {total_payout} coins total.",
                "info",
            )
        self.refresh()

    def on_next_day(self):
        prev = farm.get_state()
        farm.advance_day()
        state = farm.get_state()

        self.say(f"--- day {state['day']} begins: {state['weather_info']['label']} ---", "info")

        if state["weather"] == "storm":
            lost = state["stats"]["plants_lost"] - prev["stats"]["plants_lost"]
            if lost > 0:
                self.say(f"the storm destroyed {lost} crop(s)!", "bad")
        elif state["weather"] == "drought":
            self.say("drought — growth paused today.", "warn")

        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmGUI(root)
    root.mainloop()




