"""
gui.py — the graphical frontend. Only talks to farm.py through the 4
functions: plant(), harvest(), advance_day(), get_state(). No game rules
live here, only drawing and clicking.

Run it with:
    python3 gui.py
"""

import tkinter as tk
from tkinter import messagebox

import farm

# ---- look & feel -------------------------------------------------------

COLOR_EMPTY = "#dfd0b8"    # bare dirt
COLOR_GROWING = "#e9e28a"  # baby plant
COLOR_READY = "#8bc34a"    # ready to pick

ICON_EMPTY = ""
ICON_GROWING = "\U0001F331"   # seedling
ICON_READY = "\U0001F33E"     # sheaf of rice

BG = "#f4f1ea"


class FarmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Farm")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.plot_frames = []   # one Frame per plot, so we can recolor it
        self.plot_icons = []
        self.plot_labels = []

        self._build_status_bar()
        self._build_farm_grid()
        self._build_shop_panel()
        self._build_log()
        self._build_next_day_button()

        self.refresh()

    # ---- building the panels -------------------------------------------

    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg="#3e5c3a", pady=10)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.day_label = tk.Label(
            bar, text="", font=("Arial", 14, "bold"), bg="#3e5c3a", fg="white"
        )
        self.day_label.pack(side="left", padx=20)

        self.coins_label = tk.Label(
            bar, text="", font=("Arial", 14, "bold"), bg="#3e5c3a", fg="#ffd54f"
        )
        self.coins_label.pack(side="left", padx=20)

    def _build_farm_grid(self):
        grid = tk.Frame(self.root, bg=BG, padx=15, pady=15)
        grid.grid(row=1, column=0)

        for i in range(farm.PLOTS):
            r, c = divmod(i, 3)
            frame = tk.Frame(
                grid, width=140, height=140, bd=2, relief="ridge", bg=COLOR_EMPTY
            )
            frame.grid(row=r, column=c, padx=8, pady=8)
            frame.grid_propagate(False)

            icon = tk.Label(frame, text="", font=("Arial", 34), bg=COLOR_EMPTY)
            icon.pack(pady=(15, 0))

            label = tk.Label(frame, text="", font=("Arial", 10), bg=COLOR_EMPTY)
            label.pack()

            # clicking the frame OR either label inside it does the same thing
            for widget in (frame, icon, label):
                widget.bind("<Button-1>", lambda e, idx=i: self.on_plot_click(idx))

            self.plot_frames.append(frame)
            self.plot_icons.append(icon)
            self.plot_labels.append(label)

    def _build_shop_panel(self):
        panel = tk.Frame(self.root, bg="#fffaf0", bd=2, relief="groove", padx=12, pady=12)
        panel.grid(row=1, column=1, sticky="n", padx=(0, 15), pady=15)

        tk.Label(
            panel, text="Shop", font=("Arial", 13, "bold"), bg="#fffaf0"
        ).pack(anchor="w", pady=(0, 8))

        for name, info in farm.SHOP.items():
            row = tk.Frame(panel, bg="#fffaf0")
            row.pack(fill="x", pady=3)
            text = f"{name.title():<8} cost {info['cost']:>2}  sell {info['sell']:>2}  {info['days']}d"
            tk.Label(row, text=text, font=("Courier", 10), bg="#fffaf0", anchor="w").pack(
                fill="x"
            )

        tk.Label(
            panel, text="\nClick an empty\nplot to plant.",
            font=("Arial", 9, "italic"), bg="#fffaf0", justify="left"
        ).pack(anchor="w", pady=(10, 0))

    def _build_log(self):
        self.log = tk.Text(
            self.root, height=5, width=48, state="disabled",
            font=("Courier", 9), bg="#222", fg="#8bf28b"
        )
        self.log.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 5), sticky="ew")

    def _build_next_day_button(self):
        btn = tk.Button(
            self.root, text="Next Day \u2192", font=("Arial", 12, "bold"),
            bg="#3e5c3a", fg="white", padx=10, pady=6,
            command=self.on_next_day,
        )
        btn.grid(row=3, column=0, columnspan=2, pady=(0, 15))

    # ---- talking to the log ---------------------------------------------

    def say(self, message):
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---- redraw everything from get_state() ------------------------------

    def refresh(self):
        state = farm.get_state()

        self.day_label.config(text=f"Day {state['day']}")
        self.coins_label.config(text=f"\U0001FA99 {state['coins']} coins")

        for i, entry in enumerate(state["plots"]):
            frame = self.plot_frames[i]
            icon = self.plot_icons[i]
            label = self.plot_labels[i]

            if entry is None:
                color = COLOR_EMPTY
                icon.config(text=ICON_EMPTY, bg=color)
                label.config(text="empty", bg=color)
            elif entry["ready"]:
                color = COLOR_READY
                icon.config(text=ICON_READY, bg=color)
                label.config(text=f"{entry['crop']}\nready! click", bg=color)
            else:
                color = COLOR_GROWING
                icon.config(text=ICON_GROWING, bg=color)
                label.config(
                    text=f"{entry['crop']}\n{entry['age']}/{entry['days_needed']} days",
                    bg=color,
                )
            frame.config(bg=color)

    # ---- button/click handlers --------------------------------------------

    def on_plot_click(self, idx):
        state = farm.get_state()
        entry = state["plots"][idx]
        plot_number = idx + 1

        if entry is None:
            self.open_plant_dialog(plot_number)
        elif entry["ready"]:
            if farm.harvest(plot_number):
                payout = state["shop"][entry["crop"]]["sell"]
                self.say(f"sold {entry['crop']} from plot {plot_number} for {payout} coins.")
            else:
                self.say(f"couldn't harvest plot {plot_number}.")
            self.refresh()
        else:
            left = entry["days_needed"] - entry["age"]
            messagebox.showinfo(
                "Still growing",
                f"{entry['crop'].title()} in plot {plot_number} needs {left} more day(s)."
            )

    def open_plant_dialog(self, plot_number):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Plant in plot {plot_number}")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)

        tk.Label(
            dialog, text=f"Choose a seed for plot {plot_number}",
            font=("Arial", 11, "bold"), bg=BG
        ).pack(padx=20, pady=(15, 10))

        for name, info in farm.SHOP.items():
            text = f"{name.title()}  —  {info['cost']} coins, {info['days']} days"
            tk.Button(
                dialog, text=text, font=("Arial", 10), anchor="w",
                command=lambda n=name: self.do_plant(plot_number, n, dialog),
            ).pack(fill="x", padx=20, pady=4)

        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=(10, 15))

    def do_plant(self, plot_number, seed, dialog):
        dialog.destroy()
        if farm.plant(plot_number, seed):
            self.say(f"planted {seed} in plot {plot_number}.")
        else:
            messagebox.showwarning(
                "Can't plant that",
                "Either you don't have enough coins, or something else is wrong."
            )
        self.refresh()

    def on_next_day(self):
        farm.advance_day()
        state = farm.get_state()
        self.say(f"--- day {state['day']} begins ---")
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = FarmGUI(root)
    root.mainloop()
