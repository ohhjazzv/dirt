import random

import tkinter as tk
from tkinter import ttk, messagebox

import farm_1 as farm


BG_MAIN = "#f4f1ea"
BG_PANEL = "#fffaf0"
BG_STATUSBAR = "#3e5c3a"
BG_LOG = "#1c241c"
FG_LOG = "#8bf28b"

COLOR_EMPTY = "#dfd0b8"
COLOR_GROWING = "#e9e28a"
COLOR_STORM_RISK = "#e3b0a3"
COLOR_READY = "#8bc34a"

ICON_EMPTY = ""
ICON_GROWING = "\U0001F331"
ICON_READY = "\U0001F33E"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_HEADER = ("Arial", 13, "bold")
FONT_BODY = ("Arial", 10)
FONT_MONO = ("Courier", 10)

WEATHER_INFO = {
    "sunny": {"icon": "\u2600", "label": "Sunny", "desc": "everything grows."},
    "rain": {"icon": "\U0001F327", "label": "Rain", "desc": "everything grows."},
    "storm": {"icon": "\u26C8", "label": "Storm", "desc": "crops may be destroyed today."},
}

STAT_ROWS = [
    ("total_earned", "Total coins earned"),
    ("total_planted", "Seeds planted"),
    ("total_harvested", "Crops harvested"),
    ("best_single_sale", "Best single sale"),
    ("storms_faced", "Storms faced"),
    ("plants_lost", "Crops lost to storms"),
]

PLOT_W, PLOT_H = 150, 150
BAR_W, BAR_H = 110, 10


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

    # ------------------------------------------------------------------
    # splash
    # ------------------------------------------------------------------

    def _build_splash_screen(self):
        self.splash = tk.Frame(self.root, bg=BG_MAIN, width=500, height=420)
        self.splash.pack(fill="both", expand=True)
        self.splash.pack_propagate(False)

        tk.Label(
            self.splash, text="\U0001F33E", font=("Arial", 64), bg=BG_MAIN
        ).pack(pady=(60, 0))

        tk.Label(
            self.splash, text="Tiny Farm", font=("Georgia", 28, "bold"),
            bg=BG_MAIN, fg="#3e5c3a",
        ).pack(pady=(10, 4))

        tk.Label(
            self.splash, text="Six plots, one number going up per plant",
            font=("Arial", 11, "italic"), bg=BG_MAIN, fg="#7a7060",
        ).pack(pady=(0, 30))

        tk.Button(
            self.splash, text="Play", font=("Arial", 13, "bold"),
            activebackground="#2f3a2c", activeforeground="white",
            padx=30, pady=10, bd=0, command=self.start_game,
        ).pack()

        state = farm.get_state()
        if state["day"] > 1 or state["coins"] != farm.START_COINS:
            tk.Label(
                self.splash,
                text="continuing from day " + str(state["day"]) + ", " + str(state["coins"]) + " coins",
                font=("Arial", 9), bg=BG_MAIN, fg="#999999",
            ).pack(pady=(20, 0))

    def start_game(self):
        self.splash.destroy()
        self._build_menu_bar()
        self._build_title()
        self._build_notebook()
        self.refresh()

    def confirm_quit(self):
        if messagebox.askyesno("Quit Tiny Farm", "Your progress saves automatically. Quit now?"):
            self.root.destroy()

    # ------------------------------------------------------------------
    # chrome
    # ------------------------------------------------------------------

    def _build_menu_bar(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.confirm_quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Play", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def _build_title(self):
        title = tk.Label(
            self.root, text="\U0001F33E Tiny Farm \U0001F33E",
            font=FONT_TITLE, bg=BG_MAIN, fg="#3e5c3a", pady=10,
        )
        title.pack(fill="x")

    def _build_notebook(self):
        style = ttk.Style()
        style.configure("TNotebook", background=BG_MAIN)
        style.configure("TNotebook.Tab", font=FONT_BODY, padding=(14, 6))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        farm_tab = tk.Frame(notebook, bg=BG_MAIN)
        stats_tab = tk.Frame(notebook, bg=BG_MAIN)

        notebook.add(farm_tab, text="Farm")
        notebook.add(stats_tab, text="Stats & Achievements")

        self._build_farm_tab(farm_tab)
        self._build_stats_tab(stats_tab)

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
        bar = tk.Frame(parent, bg=BG_STATUSBAR, pady=10)
        bar.pack(fill="x")

        self.day_label = tk.Label(bar, text="", font=FONT_HEADER, bg=BG_STATUSBAR, fg="white")
        self.day_label.pack(side="left", padx=20)

        self.coins_label = tk.Label(bar, text="", font=FONT_HEADER, bg=BG_STATUSBAR, fg="#ffd54f")
        self.coins_label.pack(side="left", padx=20)

    def _build_weather_banner(self, parent):
        banner = tk.Frame(parent, bg=BG_PANEL, pady=6)
        banner.pack(fill="x", pady=(8, 4), padx=2)

        self.weather_label = tk.Label(
            banner, text="", font=("Arial", 12, "bold"), bg=BG_PANEL, anchor="w"
        )
        self.weather_label.pack(side="left", padx=14)

        self.weather_desc_label = tk.Label(
            banner, text="", font=("Arial", 10, "italic"), bg=BG_PANEL, anchor="w"
        )
        self.weather_desc_label.pack(side="left")

    # ------------------------------------------------------------------
    # farm grid
    # ------------------------------------------------------------------

    def _build_farm_grid(self, parent):
        grid = tk.Frame(parent, bg=BG_MAIN, padx=10, pady=10)
        grid.pack(side="left")

        for i in range(farm.PLOTS):
            r = i // 3
            c = i % 3

            frame = tk.Frame(
                grid, width=PLOT_W, height=PLOT_H, bd=2,
                relief="ridge", bg=COLOR_EMPTY,
            )
            frame.grid(row=r, column=c, padx=8, pady=8)
            frame.grid_propagate(False)

            icon = tk.Label(frame, text="", font=("Arial", 34), bg=COLOR_EMPTY)
            icon.pack(pady=(12, 0))

            label = tk.Label(frame, text="", font=("Arial", 10), bg=COLOR_EMPTY, justify="center")
            label.pack()

            bar_canvas = tk.Canvas(
                frame, width=BAR_W, height=BAR_H,
                bg=COLOR_EMPTY, highlightthickness=0,
            )
            bar_canvas.pack(pady=(6, 0))

            for widget in (frame, icon, label, bar_canvas):
                widget.bind("<Button-1>", lambda e, idx=i: self.on_plot_click(idx))

            self.plot_frames.append(frame)
            self.plot_icons.append(icon)
            self.plot_labels.append(label)
            self.plot_bars.append(bar_canvas)

    def _build_shop_panel(self, parent):
        panel = tk.Frame(parent, bg=BG_PANEL, bd=2, relief="groove", padx=14, pady=14)
        panel.pack(side="left", fill="y", padx=(0, 10), pady=10)

        tk.Label(panel, text="Shop", font=FONT_HEADER, bg=BG_PANEL).pack(anchor="w", pady=(0, 10))

        header = "crop        cost  sell  days   risk"
        tk.Label(panel, text=header, font=FONT_MONO, bg=BG_PANEL).pack(anchor="w")
        tk.Frame(panel, bg="#c8b89a", height=1).pack(fill="x", pady=4)

        for name in farm.SHOP:
            info = farm.SHOP[name]
            row = (
                name.ljust(12)
                + str(info["cost"]).rjust(4)
                + str(info["sell"]).rjust(6)
                + str(info["days"]).rjust(6)
                + (str(int(info["risk"] * 100)) + "%").rjust(7)
            )
            tk.Label(panel, text=row, font=FONT_MONO, bg=BG_PANEL, anchor="w").pack(anchor="w", pady=1)

        tk.Label(
            panel,
            text="\nrisk = chance a storm\ndestroys that crop.\n\nClick an empty plot\nto plant something.",
            font=("Arial", 9, "italic"), bg=BG_PANEL, justify="left",
        ).pack(anchor="w", pady=(14, 0))

    def _build_log(self, parent):
        self.log = tk.Text(
            parent, height=6, bg=BG_LOG, fg=FG_LOG,
            font=FONT_MONO, bd=0, state="disabled", wrap="word",
        )
        self.log.pack(fill="x", padx=12, pady=(4, 0))

    def _build_action_buttons(self, parent):
        row = tk.Frame(parent, bg=BG_MAIN)
        row.pack(pady=10)

        harvest_all_btn = tk.Button(
            row, text="Harvest All \u2663", font=("Arial", 12, "bold"),
            bg=COLOR_READY, fg="#2c3e1a", activebackground="#79a83f",
            padx=12, pady=8, bd=0, command=self.on_harvest_all,
        )
        harvest_all_btn.pack(side="left", padx=(0, 10))

        next_day_btn = tk.Button(
            row, text="Next Day \u2192", font=("Arial", 12, "bold"),
            bg=BG_STATUSBAR, fg="white", activebackground="#2f4a2c",
            activeforeground="white", padx=12, pady=8, bd=0,
            command=self.on_next_day,
        )
        next_day_btn.pack(side="left")

    # ------------------------------------------------------------------
    # stats tab
    # ------------------------------------------------------------------

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

        for key, label_text in STAT_ROWS:
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

        for name in farm.get_state()["achievements"]:
            row = tk.Frame(panel, bg=BG_PANEL)
            row.pack(fill="x", pady=3, anchor="w")

            lbl = tk.Label(
                row, text="\U0001F512  " + name, font=FONT_BODY, bg=BG_PANEL, anchor="w"
            )
            lbl.pack(anchor="w")
            self.achievement_labels[name] = lbl

    # ------------------------------------------------------------------
    # dialogs
    # ------------------------------------------------------------------

    def show_help(self):
        messagebox.showinfo(
            "How to Play",
            "Click an empty plot to buy and plant a seed.\n"
            "Click a growing plot to see how many days are left.\n"
            "Click a ready (green) plot to harvest and sell it.\n"
            "Press 'Next Day' to move time forward.\n\n"
            "Watch the weather banner. Storms can destroy crops.\n\n"
            "Your progress saves automatically."
        )

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Tiny Farm\n\nA tiny farming game.\n"
            "Logic lives in farm_1.py. This window is just the face."
        )

    # ------------------------------------------------------------------
    # log
    # ------------------------------------------------------------------

    def say(self, message, kind="info"):
        colors = {"info": FG_LOG, "warn": "#f2c94c", "bad": "#f28b8b"}
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        line_start = self.log.index("end-2l")
        line_end = self.log.index("end-1l")
        tag = "tag_" + kind
        self.log.tag_configure(tag, foreground=colors.get(kind, FG_LOG))
        self.log.tag_add(tag, line_start, line_end)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ------------------------------------------------------------------
    # redraw from get_state() — the only source of truth
    # ------------------------------------------------------------------

    def refresh(self):
        state = farm.get_state()

        self.day_label.config(text="Day " + str(state["day"]))
        self.coins_label.config(text="\U0001FA99 " + str(state["coins"]) + " coins")

        wi = WEATHER_INFO.get(state["weather"], WEATHER_INFO["sunny"])
        self.weather_label.config(text=wi["icon"] + " " + wi["label"])
        self.weather_desc_label.config(text=wi["desc"])

        is_storm_day = state["weather"] == "storm"

        for i in range(len(state["plots"])):
            entry = state["plots"][i]
            frame = self.plot_frames[i]
            icon = self.plot_icons[i]
            label = self.plot_labels[i]
            bar = self.plot_bars[i]

            bar.delete("all")

            if entry is None:
                color = COLOR_EMPTY
                icon.config(text=ICON_EMPTY, bg=color)
                label.config(text="empty\nclick to plant", bg=color)

            elif entry["ready"]:
                color = COLOR_READY
                icon.config(text=ICON_READY, bg=color)
                label.config(text=entry["crop"] + "\nready! click", bg=color)
                bar.create_rectangle(0, 0, BAR_W, BAR_H, fill="#4a7a2c", outline="")

            else:
                color = COLOR_STORM_RISK if is_storm_day else COLOR_GROWING
                icon.config(text=ICON_GROWING, bg=color)

                extra = ""
                if is_storm_day:
                    risk = farm.SHOP[entry["crop"]]["risk"]
                    extra = "\n" + str(int(risk * 100)) + "% storm risk"

                label.config(
                    text=entry["crop"] + "\n" + str(entry["age"]) + "/" + str(entry["days_needed"]) + " days" + extra,
                    bg=color,
                )
                ratio = entry["age"] / entry["days_needed"]
                bar.create_rectangle(0, 0, BAR_W, BAR_H, outline="#8a7a5c")
                bar.create_rectangle(0, 0, int(BAR_W * ratio), BAR_H, fill="#c9a227", outline="")

            bar.config(bg=color)
            frame.config(bg=color)

        stats = state["stats"]
        for key in self.stat_value_labels:
            self.stat_value_labels[key].config(text=str(stats[key]))

        achievements = state["achievements"]
        for name in self.achievement_labels:
            lbl = self.achievement_labels[name]
            if achievements.get(name):
                lbl.config(text="\u2705  " + name, fg="#2e7d32")
            else:
                lbl.config(text="\U0001F512  " + name, fg="#999999")

    # ------------------------------------------------------------------
    # handlers — these call farm_1 and nothing else
    # ------------------------------------------------------------------

    def on_plot_click(self, idx):
        state = farm.get_state()
        entry = state["plots"][idx]
        plot_number = idx + 1

        if entry is None:
            self.open_plant_dialog(plot_number)

        elif entry["ready"]:
            result = farm.harvest(plot_number)
            self.say(result["message"], "info" if result["ok"] else "bad")
            self.refresh()
            if result["ok"]:
                self.confetti()

        else:
            left = entry["days_needed"] - entry["age"]
            messagebox.showinfo(
                "Still growing",
                entry["crop"] + " in plot " + str(plot_number) + " needs " + str(left) + " more day(s)."
            )

    def open_plant_dialog(self, plot_number):
        state = farm.get_state()
        coins = state["coins"]

        dialog = tk.Toplevel(self.root)
        dialog.title("Plant in plot " + str(plot_number))
        dialog.configure(bg=BG_MAIN)
        dialog.resizable(False, False)

        tk.Label(
            dialog, text="Choose a seed for plot " + str(plot_number),
            font=FONT_HEADER, bg=BG_MAIN,
        ).pack(padx=20, pady=(15, 10))

        for name in farm.SHOP:
            info = farm.SHOP[name]
            afford = coins >= info["cost"]
            text = name.ljust(12) + str(info["cost"]).rjust(3) + " coins   " + str(info["days"]) + " days"
            btn = tk.Button(
                dialog, text=text, font=FONT_MONO, anchor="w",
                state="normal" if afford else "disabled",
                command=lambda n=name: self.do_plant(plot_number, n, dialog),
            )
            btn.pack(fill="x", padx=20, pady=3)

        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=(12, 15))

    def do_plant(self, plot_number, seed, dialog):
        dialog.destroy()
        result = farm.plant(plot_number, seed)
        if result["ok"]:
            self.say(result["message"], "info")
        else:
            messagebox.showwarning("Can't plant that", result["message"])
        self.refresh()

    def on_harvest_all(self):
        state = farm.get_state()
        harvested = 0

        for i in range(len(state["plots"])):
            entry = state["plots"][i]
            if entry is not None and entry["ready"]:
                result = farm.harvest(i + 1)
                if result["ok"]:
                    self.say(result["message"], "info")
                    harvested = harvested + 1

        if harvested == 0:
            self.say("nothing ready to harvest.", "warn")

        self.refresh()

        if harvested > 0:
            self.confetti()

    def on_next_day(self):
        before = farm.get_state()["achievements"]
        result = farm.advance_day()
        state = farm.get_state()

        wi = WEATHER_INFO.get(state["weather"], WEATHER_INFO["sunny"])
        self.say("--- day " + str(state["day"]) + " begins: " + wi["label"] + " ---", "info")

        for event in result["events"]:
            self.say(event, "bad")

        after = state["achievements"]
        for name in after:
            if after[name] and not before.get(name):
                self.say("achievement unlocked: " + name, "warn")

        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmGUI(root)
    root.mainloop()

