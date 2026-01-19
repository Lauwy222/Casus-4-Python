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

# Segment COM locations as fractions of segment length measured from distal end
SHANK_POS = 0.565
THIGH_POS = 0.565
TRUNK_POS = 0.300

# Head drawing
HEAD_RADIUS = 11.0

# Mass percentages (from the table in the handout), converted to fractions
# Note:
# - Our model has one leg representing two legs => leg segment fractions multiplied by 2
# - Trunk and arms are combined; arms exist twice (left+right) => arm fractions multiplied by 2
MALE = {
    "head": 0.0896,
    "trunk_arms": 0.4684 + 2.0 * (0.0325 + 0.0187 + 0.0065),
    "thigh": 2.0 * 0.1050,
    "shank": 2.0 * 0.0475,
    "foot": 2.0 * 0.0143,
}
FEMALE = {
    "head": 0.0820,
    "trunk_arms": 0.4500 + 2.0 * (0.0290 + 0.0157 + 0.0050),
    "thigh": 2.0 * 0.1175,
    "shank": 2.0 * 0.0535,
    "foot": 2.0 * 0.0133,
}

#%% S3 - Other functions
def sind(angle_deg):
    """Return sine of an angle given in degrees (uses numpy)."""
    return np.sin(np.deg2rad(angle_deg))

def cosd(angle_deg):
    """Return cosine of an angle given in degrees (uses numpy)."""
    return np.cos(np.deg2rad(angle_deg))

#%% S4 - Model calculation and plotting
def calculate_model(*_):
    # Subsection: read joint angles
    ankle_ang = ankle_slider.get()
    knee_ang = knee_slider.get()
    hip_ang = hip_slider.get()

    # Subsection: read segment lengths (floats)
    foot_len = foot_var.get()
    shank_len = shank_var.get()
    thigh_len = thigh_var.get()
    trunk_len = trunk_var.get()

    # Subsection: compute body key points (forward kinematics)
    heel = np.array([0.0, 0.0])

    toe = np.array([
        heel[0] + foot_len,
        0.0
    ])

    ankle = np.array([
        heel[0] + foot_len / 5.0,
        heel[1] + foot_len / 4.0
    ])

    # Shank (ankle -> knee)
    knee = ankle + np.array([
        cosd(ankle_ang) * shank_len,
        sind(ankle_ang) * shank_len
    ])

    # Thigh (knee -> hip)
    thigh_ang = 180.0 - (knee_ang - ankle_ang)
    hip = knee + np.array([
        cosd(thigh_ang) * thigh_len,
        sind(thigh_ang) * thigh_len
    ])

    # Trunk (hip -> head)
    purple_ang = knee_ang - ankle_ang
    trunk_ang = hip_ang - purple_ang
    head = hip + np.array([
        cosd(trunk_ang) * trunk_len,
        sind(trunk_ang) * trunk_len
    ])

    # Subsection: head circle
    head_circle = plt.Circle(
        (head[0], head[1]),
        radius=HEAD_RADIUS,
        edgecolor="blue",
        facecolor="white",
        zorder=2
    )

    # Subsection: segment COM points
    # Foot COM: x at 1/3 of foot length from heel, y at 1/3 of foot height
    foot_height = foot_len / 4.0
    cm_foot = np.array([
        heel[0] + foot_len / 3.0,
        heel[1] + foot_height / 3.0
    ])

    # Shank COM from distal end (ankle) along shank direction
    cm_shank = ankle + np.array([
        cosd(ankle_ang) * shank_len * SHANK_POS,
        sind(ankle_ang) * shank_len * SHANK_POS
    ])

    # Thigh COM from distal end (knee) along thigh direction
    cm_thigh = knee + np.array([
        cosd(thigh_ang) * thigh_len * THIGH_POS,
        sind(thigh_ang) * thigh_len * THIGH_POS
    ])

    # Trunk COM from distal end (hip) along trunk direction
    cm_trunk = hip + np.array([
        cosd(trunk_ang) * trunk_len * TRUNK_POS,
        sind(trunk_ang) * trunk_len * TRUNK_POS
    ])

    # Head COM: use head point
    cm_head = head.copy()

    # Subsection: select mass fractions (male/female)
    if radio_var.get() == 1:
        mf = MALE
    else:
        mf = FEMALE

    # Subsection: whole-body COM (weighted average)
    total_mass_frac = mf["foot"] + mf["shank"] + mf["thigh"] + mf["trunk_arms"] + mf["head"]
    cm_body = (
        mf["foot"] * cm_foot
        + mf["shank"] * cm_shank
        + mf["thigh"] * cm_thigh
        + mf["trunk_arms"] * cm_trunk
        + mf["head"] * cm_head
    ) / total_mass_frac

    # Subsection: update coordinate label text
    txt = f"x = {cm_body[0]:.2f}\ny = {cm_body[1]:.2f}"
    cmval_lbl.config(text=txt)

    # Subsection: balance / fall detection (label background color)
    # green: between ankle and toe
    # orange: behind ankle but in front of heel
    # red: outside support area
    if (cm_body[0] > ankle[0]) and (cm_body[0] < toe[0]):
        cmval_lbl.config(bg="#b6f2b6")  # light green
    elif (cm_body[0] < ankle[0]) and (cm_body[0] > heel[0]):
        cmval_lbl.config(bg="#ffcc99")  # orange
    else:
        cmval_lbl.config(bg="#ff9999")  # light red

    # Subsection: draw
    figure1.clear()
    ax1 = figure1.add_subplot(1, 1, 1)

    # Foot (blue)
    ax1.plot([heel[0], toe[0]],   [heel[1], toe[1]],   "b-")  # heel -> toe
    ax1.plot([heel[0], ankle[0]], [heel[1], ankle[1]], "b-")  # heel -> ankle
    ax1.plot([ankle[0], toe[0]],  [ankle[1], toe[1]],  "b-")  # ankle -> toe

    # Shank, thigh, trunk (blue)
    ax1.plot([ankle[0], knee[0]], [ankle[1], knee[1]], "b-")  # ankle -> knee
    ax1.plot([knee[0], hip[0]],   [knee[1], hip[1]],   "b-")  # knee -> hip
    ax1.plot([hip[0], head[0]],   [hip[1], head[1]],   "b-")  # hip -> head

    # Head circle (draw before plotting cm_head dot so the red dot stays visible on top)
    ax1.add_artist(head_circle)

    # Segment COM points (red)
    ax1.plot(cm_foot[0],  cm_foot[1],  "ro", zorder=3)
    ax1.plot(cm_shank[0], cm_shank[1], "ro", zorder=3)
    ax1.plot(cm_thigh[0], cm_thigh[1], "ro", zorder=3)
    ax1.plot(cm_trunk[0], cm_trunk[1], "ro", zorder=3)
    ax1.plot(cm_head[0],  cm_head[1],  "ro", zorder=3)

    # Whole-body COM (red dot, markersize 5)
    ax1.plot(cm_body[0], cm_body[1], "ro", markersize=5, zorder=4)

    # Vertical projection line from cm_body to x-axis (red dashed)
    ax1.plot([cm_body[0], cm_body[0]], [0.0, cm_body[1]], "r--", zorder=1)

    # Plot formatting
    ax1.set_xlim(-75, 100)
    ax1.set_ylim(-10, 200)
    ax1.set_aspect("equal", adjustable="box")

    canvas.draw()

#%% S5 - Create GUI elements
root = tk.Tk()
root.geometry("1000x750")
root.resizable(False, False)
root.title("Squat Gui")

# Embedded matplotlib figure
figure1 = plt.Figure(figsize=(4, 4), dpi=150, facecolor="#d9d9d9")
canvas = FigureCanvasTkAgg(figure1, master=root)
canvas_widget = canvas.get_tk_widget()

# Logo (robust path handling)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "asset", "btlogo.png")

try:
    pict = tk.PhotoImage(file=LOGO_PATH)
    pict_lbl = tk.Label(master=root, image=pict)
    pict_lbl.image = pict
except tk.TclError:
    pict_lbl = tk.Label(master=root, text="(logo not found)")

# Sliders
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

# Entries (segment lengths)
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

# Radiobuttons (male/female)
radio_var = tk.IntVar(value=1)  # 1 = male, 2 = female
radio_frame = tk.Frame(master=root, width=300, height=30)

male_radio = tk.Radiobutton(
    master=radio_frame, text="Male", variable=radio_var, value=1, command=calculate_model
)
female_radio = tk.Radiobutton(
    master=radio_frame, text="Female", variable=radio_var, value=2, command=calculate_model
)

# Labels to show cm_body coordinates
cmtxt_lbl = tk.Label(master=root, text="Body COM (cm_body)")
cmval_lbl = tk.Label(master=root, text="x = 0.00\ny = 0.00", bg="white", width=12, justify="left")

#%% S6 - Place GUI elements
canvas_widget.pack(side="right", fill="y")

# Left side (top-to-bottom)
pict_lbl.pack(side="top", pady=5)

# Body COM labels (must be under logo, above entries)
cmtxt_lbl.pack(side="top", pady=(5, 0))
cmval_lbl.pack(side="top", pady=(0, 8))

# Radiobuttons
radio_frame.pack(side="top", pady=5)
male_radio.pack(side="left")
female_radio.pack(side="left")

# Entries + labels (label above entry)
foot_lbl.pack(side="top", pady=(10, 0))
foot_entry.pack(side="top", pady=(0, 5))

shank_lbl.pack(side="top", pady=(10, 0))
shank_entry.pack(side="top", pady=(0, 5))

thigh_lbl.pack(side="top", pady=(10, 0))
thigh_entry.pack(side="top", pady=(0, 5))

trunk_lbl.pack(side="top", pady=(10, 0))
trunk_entry.pack(side="top", pady=(0, 5))

# Sliders at the bottom
hip_slider.pack(side="bottom", pady=5)
knee_slider.pack(side="bottom", pady=5)
ankle_slider.pack(side="bottom", pady=(10, 30))

# Initial draw
calculate_model()

#%% S7 - Event loop
root.mainloop()
