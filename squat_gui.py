# -*- coding: utf-8 -*-
"""
Squat GUI - page 7/8 state
This script contains:
- 3 sliders (ankle, knee, hip) connected to calculate_model()
- 4 Entry widgets (foot, shank, thigh, trunk) using tk.DoubleVar
- Page 8: foot geometry (heel, toe, ankle) plotted as blue line segments
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

#%% S3 - Other functions
#%% S3 - Other functions
def sind(angle_deg):
   return np.sin(np.deg2rad(angle_deg))

def cosd(angle_deg):
    return np.cos(np.deg2rad(angle_deg))

#%% S4 - Model calculation and plotting
def calculate_model(*_):
    # Subsection: read joint angles from sliders (not used yet on page 8)
    ankle_ang = ankle_slider.get()
    knee_ang = knee_slider.get()
    hip_ang = hip_slider.get()

    # Subsection: read segment lengths as numeric values (floats)
    foot_len = foot_var.get()
    shank_len = shank_var.get()
    thigh_len = thigh_var.get()
    trunk_len = trunk_var.get()

    # Subsection: compute foot key points (page 8)
    heel = np.array([0.0, 0.0])

    toe = np.array([
        heel[0] + foot_len,
        0.0
    ])

    ankle = np.array([
        heel[0] + foot_len / 5.0,
        heel[1] + foot_len / 4.0
    ])
    
    # Subsection: Calc dist_x leg
    dist_x =  cosd(ankle_ang)*shank_len
    
    # Subsection: Calc dist_y leg
    dist_y = sind(ankle_ang) * shank_len
    
    # Subsection: Calc kneepoint    
    knee = ankle + np.array([dist_x, dist_y])
    
    # Subsection: Calc Thigh angle
    thigh_ang = 180-(knee_ang-ankle_ang)
    
    # Subsection: Thigh segment components
    dist_x_thigh = cosd(thigh_ang) * thigh_len
    dist_y_thigh = sind(thigh_ang) * thigh_len
    
    # Subsection: Hip position
    hip = knee + np.array([dist_x_thigh, dist_y_thigh])
    
    # Subsection: trunk (hip -> head)

    # Shared relative angle used in the handout diagrams
    purple_ang = knee_ang - ankle_ang

    # Absolute trunk angle with respect to the positive x-axis
    trunk_ang = hip_ang - purple_ang

    # Trunk segment components
    dist_x_trunk = cosd(trunk_ang) * trunk_len
    dist_y_trunk = sind(trunk_ang) * trunk_len

    # Head point (end of trunk)
    head = hip + np.array([dist_x_trunk, dist_y_trunk])

    # Subsection: clear and rebuild the plot area
    figure1.clear()
    ax1 = figure1.add_subplot(1, 1, 1)

    # Subsection: draw foot as blue line segments
    # Segment 1: heel -> toe (sole)
    ax1.plot([heel[0], toe[0]], [heel[1], toe[1]], "b-")

    # Segment 2: heel -> ankle
    ax1.plot([heel[0], ankle[0]], [heel[1], ankle[1]], "b-")

    # Segment 3: ankle -> toe
    ax1.plot([ankle[0], toe[0]], [ankle[1], toe[1]], "b-")
    
    # Segment 4: Ankle -> Knee
    ax1.plot([ankle[0], knee[0]], [ankle[1], knee[1]], "b-")
    
    # Segent 5: Plot thigh as a blue line
    ax1.plot([knee[0], hip[0]], [knee[1], hip[1]], "b-")

    # Segmment 6: Plot trunk as a blue line
    ax1.plot([hip[0], head[0]], [hip[1], head[1]], "b-")

    # Subsection: axis limits and aspect ratio
    # Use limits that make the foot visible for typical foot lengths
    ax1.set_xlim(-75, 100)
    ax1.set_ylim(-10, 200)
    ax1.set_aspect("equal", adjustable="box")

    # Subsection: redraw canvas
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
canvas_widget.pack(side="right", fill="y")

pict_lbl.pack(side="top", pady=5)

foot_lbl.pack(side="top", pady=(10, 0))
foot_entry.pack(side="top", pady=(0, 5))

shank_lbl.pack(side="top", pady=(10, 0))
shank_entry.pack(side="top", pady=(0, 5))

thigh_lbl.pack(side="top", pady=(10, 0))
thigh_entry.pack(side="top", pady=(0, 5))

trunk_lbl.pack(side="top", pady=(10, 0))
trunk_entry.pack(side="top", pady=(0, 5))

hip_slider.pack(side="bottom", pady=5)
knee_slider.pack(side="bottom", pady=5)
ankle_slider.pack(side="bottom", pady=(10, 30))

# Subsection: initial draw
calculate_model()

#%% S7 - Event loop
root.mainloop()
