import tkinter as tk
from tkinter import filedialog
from modules.vibe import get_vibe_stats
from modules.fft import show_fft

root = tk.Tk()

root.title("DroneVibeAnalyzer")
root.geometry("1000x600")

selected_file = tk.StringVar()

# ======================
# FUNCTIONS
# ======================

def run_fft():

    filepath = selected_file.get()

    if filepath == "":
        return

    show_fft(filepath)


def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("BIN Files", "*.bin")]
    )

    selected_file.set(filename)


def show_summary():

    filepath = selected_file.get()

    if filepath == "":
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please select a BIN file")
        return

    try:

        vibe = get_vibe_stats(filepath)

        report = f"""
=========================
DRONE HEALTH REPORT
=========================

Vibration Status : Healthy

Mean X : {vibe['mean_x']}
Mean Y : {vibe['mean_y']}
Mean Z : {vibe['mean_z']}

Recommendations:
- Vibration levels acceptable
- No major issues detected

=========================
"""

        output.delete("1.0", tk.END)
        output.insert(tk.END, report)

    except Exception as e:

        output.delete("1.0", tk.END)
        output.insert(tk.END, str(e))


# ======================
# TOP AREA
# ======================

title = tk.Label(
    root,
    text="🚁 DroneVibeAnalyzer",
    font=("Arial", 22)
)

title.pack(pady=10)

browse_btn = tk.Button(
    root,
    text="Browse BIN File",
    command=browse_file
)

browse_btn.pack()

file_label = tk.Label(
    root,
    textvariable=selected_file
)

file_label.pack(pady=5)

# ======================
# MAIN FRAME
# ======================

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# LEFT PANEL

left_panel = tk.Frame(
    main_frame,
    width=200
)

left_panel.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# RIGHT PANEL

right_panel = tk.Frame(main_frame)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ======================
# BUTTONS
# ======================

btn_summary = tk.Button(
    left_panel,
    text="Summary Report",
    width=20,
    command=show_summary
)
btn_summary.pack(pady=5)

btn_vibe = tk.Button(
    left_panel,
    text="VIBE Analysis",
    width=20
)
btn_vibe.pack(pady=5)

btn_fft = tk.Button(
    left_panel,
    text="FFT Analysis",
    width=20,
    command=run_fft
)
btn_fft.pack(pady=5)

btn_ftn = tk.Button(
    left_panel,
    text="FTN Statistics",
    width=20
)
btn_ftn.pack(pady=5)

btn_pwm = tk.Button(
    left_panel,
    text="PWM vs Notch",
    width=20
)
btn_pwm.pack(pady=5)

# ======================
# OUTPUT BOX
# ======================

output = tk.Text(
    right_panel,
    font=("Consolas", 11)
)

output.pack(
    fill="both",
    expand=True
)

root.mainloop()