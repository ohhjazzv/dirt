import tkinter as tk
from tkinter import messagebox

import farm_1

# setting
COLOR_EMPTY = "#dfd0b8" #dirt
COLOR_GROWING = "#ee28a" #baby plant
COLOR_READY = "#8bc34a" # Symboling readyu to pick

ICON_EMPTY = ""
ICON_GROWING = "\U0001F331" #seeding
ICON_READY = "\U0001F33E" # sheaf of rice

BG = "#f4f1ea"


class FarmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiny Farm")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.plot_frames = []
        self.plot_icons = []
        self.plot_labels = []
        self._build_status_bar()
        self._build_farm_grid()
        self._build_shop_panel()
        self._build_log()
        self._build_next_day_button()
        self.refresh() 



    def _build_status_bat(self):
        bar = tk.Frame(self.root, bg = "#3e5c3a", pady = 10)
        bar.grid(row = 0, column = 0, columnspan = 2, sticky = "ew")

        self.day_label = tk.label(
            bar, text = "", font = ("Arial", 12, "bold"),  bg = "#3e5c3a", fg = "white")
        self.day_label.pack(side="left", padx=20)
        self.coins_label = tk.label(bar, text ="", font = ("Arial", 14, "bold"), bg = "#3e5c3a", fg="#ffd54f" )
        self.coins_label.pack(side = "left", padx = 20)




    def _build_farm_grid(self):
        grid = tk.Frame(self.root, bg = BG, padx = 15, pady = 15)
        grid.grid(row=1, column=0)

        for i in range(farm.PLOTS):