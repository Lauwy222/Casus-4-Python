# -*- coding: utf-8 -*-
"""
Squat GUI - base structure (page 3)
This script prepares the GUI layout and verifies communication
between the slider and the calculate_model() function.
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

#%% S3 - Other functions
# Placeholder section for helper functions (e.g., sind(), cosd()) introduced later.

#%% S4 - Model calculation and plotting
def calculate_model(*_):
    """
    Callback function for GUI changes.
    At this stage it only redraws an empty plot area to confirm that the GUI
    triggers this function correctly.
    """

    # Subsection: read current GUI state
    ankle_ang = ankle_slider.get()

    # Subsection: clear and rebuild the plot
    figure1.clear()
    ax1 = figure1.add_subplot(1, 1, 1)

    # Subsection: keep a visible reserved plot area
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect("equal", adjustable="box")

    # Subsection: diagnostic output in the figure (temporary for page 3)
    ax1.set_title(f"Ankle angle = {ankle_ang}°")

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

# Subsection: logo (robust path handling for Spyder / different working directories)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "asset", "btlogo.png")

pict_lbl = None
try:
    pict = tk.PhotoImage(file=LOGO_PATH)
    pict_lbl = tk.Label(master=root, image=pict)
    # Keep a Python reference to prevent Tkinter image garbage collection
    pict_lbl.image = pict
except tk.TclError:
    # If the image cannot be loaded, continue without the logo
    pict_lbl = tk.Label(master=root, text="(logo not found)")

# Subsection: ankle slider
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

#%% S6 - Place GUI elements
# Subsection: plot placement
canvas_widget.pack(side="right", fill="y")

# Subsection: left-side controls placement (top-to-bottom order)
pict_lbl.pack(side="top", pady=10)
ankle_slider.pack(side="bottom", pady=(10, 60))

# Subsection: initial draw
calculate_model()

#%% S7 - Event loop
root.mainloop()
