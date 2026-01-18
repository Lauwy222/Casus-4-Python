# -*- coding: utf-8 -*-
"""
Squat GUI - page 7 state
This script contains:
- 3 sliders (ankle, knee, hip) connected to calculate_model()
- 4 Entry widgets (foot, shank, thigh, trunk) using tk.DoubleVar
- Proper event binding: pressing Enter in an Entry triggers calculate_model()
"""

#%% S1 - Libraries
import os
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

#%% S2 - Initial values / constants
INITIAL_ANKLE_ANG = 60
INITIAL_KNEE_ANG = 90
INITIAL_HIP_ANG = 90

INITIAL_FOOT_LEN = 28.0
INITIAL_SHANK_LEN = 50.0
INITIAL_THIGH_LEN = 50.0
INITIAL_TRUNK_LEN = 80.0
toe = [0,0]

#%% S3 - Other functions
# Placeholder for helper functions introduced later (e.g., sind(), cosd()).

#%% S4 - Model calculation and plotting
def calculate_model(*_):    
    # Subsection: read joint angles from sliders
    ankle_ang = ankle_slider.get()
    knee_ang = knee_slider.get()
    hip_ang = hip_slider.get()

    # Subsection: read segment lengths as numeric values (floats)
    foot_len = foot_var.get()
    shank_len = shank_var.get()
    thigh_len = thigh_var.get()
    trunk_len = trunk_var.get()

    heel = np.array([0.0, 0.0])
    toe = np.array([
    heel[0] + foot_len,0.0
])
    ankle = np.array([
    heel[0] + foot_len / 5,heel[1] + foot_len / 4
])


    # Subsection: clear and rebuild the plot area
    figure1.clear()
    ax1 = figure1.add_subplot(1, 1, 1)

    # Subsection: keep a visible reserved plot area (temporary for early stages)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect("equal", adjustable="box")

    canvas.draw()

#%% S5 - Create GUI elements
# Subsection: main window
root = tk.Tk()
root.geometry("1000x750")
root.resizable(False, False)
root.title("Squat Gui")

# Subsection: embedded matplotlib figure
figure1 = plt.Figure(figsize=(4, 4), dpi=150, facecolor="#d9d9d9")
canvas = FigureCanvasTkAgg(figure1, master=root)
canvas_widget = canvas.get_tk_widget()

# Subsection: logo (robust path handling for different working directories)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "asset", "btlogo.png")

try:
    pict = tk.PhotoImage(file=LOGO_PATH)
    pict_lbl = tk.Label(master=root, image=pict)
    # Keep a Python reference to prevent image garbage collection
    pict_lbl.image = pict
except tk.TclError:
    pict_lbl = tk.Label(master=root, text="(logo not found)")

# Subsection: sliders
# Ankle slider can safely attach command immediately
ankle_slider = tk.Scale(
    master=root,
    from_=30,
    to=130,
    label="Ankle angle",
    resolution=1,
    length=200,
    orient="horizontal",
    command=calculate_model
)
ankle_slider.set(INITIAL_ANKLE_ANG)

# Knee slider: attach command only after set() to prevent extra redraw at startup
knee_slider = tk.Scale(
    master=root,
    from_=10,
    to=180,
    label="Knee angle",
    resolution=1,
    length=200,
    orient="horizontal"
)
knee_slider.set(INITIAL_KNEE_ANG)
knee_slider.config(command=calculate_model)

# Hip slider: attach command only after set() to prevent extra redraw at startup
hip_slider = tk.Scale(
    master=root,
    from_=30,
    to=180,
    label="Hip angle",
    resolution=1,
    length=200,
    orient="horizontal"
)
hip_slider.set(INITIAL_HIP_ANG)
hip_slider.config(command=calculate_model)

# Subsection: Entry widgets for segment lengths (tk.DoubleVar provides numeric values)
foot_var = tk.DoubleVar(value=INITIAL_FOOT_LEN)
foot_entry = tk.Entry(master=root, width=6, textvariable=foot_var)
foot_entry.bind("<Return>", calculate_model)
foot_lbl = tk.Label(master=root, text="Foot length")

shank_var = tk.DoubleVar(value=INITIAL_SHANK_LEN)
shank_entry = tk.Entry(master=root, width=6, textvariable=shank_var)
shank_entry.bind("<Return>", calculate_model)
shank_lbl = tk.Label(master=root, text="Shank length")

thigh_var = tk.DoubleVar(value=INITIAL_THIGH_LEN)
thigh_entry = tk.Entry(master=root, width=6, textvariable=thigh_var)
thigh_entry.bind("<Return>", calculate_model)
thigh_lbl = tk.Label(master=root, text="Thigh length")

trunk_var = tk.DoubleVar(value=INITIAL_TRUNK_LEN)
trunk_entry = tk.Entry(master=root, width=6, textvariable=trunk_var)
trunk_entry.bind("<Return>", calculate_model)
trunk_lbl = tk.Label(master=root, text="Trunk length")

#%% S6 - Place GUI elements
# Subsection: plot placement
canvas_widget.pack(side="right", fill="y")

# Subsection: left-side placement (top-to-bottom)
pict_lbl.pack(side="top", pady=5)

# Entries and labels (label above entry)
foot_lbl.pack(side="top", pady=(10, 0))
foot_entry.pack(side="top", pady=(0, 5))

shank_lbl.pack(side="top", pady=(10, 0))
shank_entry.pack(side="top", pady=(0, 5))

thigh_lbl.pack(side="top", pady=(10, 0))
thigh_entry.pack(side="top", pady=(0, 5))

trunk_lbl.pack(side="top", pady=(10, 0))
trunk_entry.pack(side="top", pady=(0, 5))

# Sliders at the bottom (packing bottom gives correct visual order)
ankle_slider.pack(side="bottom", pady=(10, 30))
knee_slider.pack(side="bottom", pady=5)
hip_slider.pack(side="bottom", pady=5)

# Subsection: initial draw
calculate_model()

#%% S7 - Event loop
root.mainloop()
