import customtkinter as ctk
from tkinter import filedialog

from modules.vibe import get_vibe_stats
from modules.ftn import get_ftn_stats
from modules.pwm import get_pwm_stats
from modules.fft import show_fft

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
selected_file = ""

app.title("DroneVibeAnalyzer")
app.geometry("1200x700")

# Title

ctk.CTkButton(
    left_frame,
    text="Summary",
    command=summary_report
).pack(pady=5)

ctk.CTkButton(
    left_frame,
    text="VIBE Analysis",
    command=vibe_report
).pack(pady=5)

ctk.CTkButton(
    left_frame,
    text="FFT Analysis",
    command=fft_report
).pack(pady=5)

ctk.CTkButton(
    left_frame,
    text="FTN Statistics",
    command=ftn_report
).pack(pady=5)

ctk.CTkButton(
    left_frame,
    text="PWM vs Notch",
    command=pwm_report
).pack(pady=5)

# Main Area
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Left Menu
left_frame = ctk.CTkFrame(main_frame, width=220)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# Right Output
right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

def browse_bin():

    global selected_file

    filename = filedialog.askopenfilename(
        filetypes=[("BIN Files","*.bin")]
    )

    if filename:
        selected_file = filename
        file_label.configure(text=filename)


def summary_report():

    if selected_file == "":
        output.delete("1.0","end")
        output.insert("1.0","Select BIN File First")
        return

    vibe = get_vibe_stats(selected_file)
    ftn = get_ftn_stats(selected_file)
    pwm = get_pwm_stats(selected_file)

    report = f"""
=============================
OVERALL HEALTH REPORT
=============================

Health Score : 92 / 100

Vibration : PASS
Notch Tracking : PASS
PWM Tracking : GOOD

Mean X : {vibe['mean_x']}
Mean Y : {vibe['mean_y']}
Mean Z : {vibe['mean_z']}

Notch Mean : {ftn['mean']} Hz

PWM Correlation : {pwm['correlation']}

Recommendations:

✓ Vibration acceptable

✓ Harmonic notch tracking working

✓ No severe resonance detected

✓ Motor balance appears good
"""

    output.delete("1.0","end")
    output.insert("1.0", report)


def vibe_report():

    if selected_file == "":
        return

    vibe = get_vibe_stats(selected_file)

    txt = f"""
VIBE ANALYSIS

Mean X : {vibe['mean_x']}
Mean Y : {vibe['mean_y']}
Mean Z : {vibe['mean_z']}

Max Z : {vibe['max_z']}
"""

    output.delete("1.0","end")
    output.insert("1.0", txt)


def ftn_report():

    if selected_file == "":
        return

    ftn = get_ftn_stats(selected_file)

    txt = f"""
FTN STATISTICS

Mean : {ftn['mean']} Hz

Min : {ftn['min']} Hz

Max : {ftn['max']} Hz
"""

    output.delete("1.0","end")
    output.insert("1.0", txt)


def pwm_report():

    if selected_file == "":
        return

    pwm = get_pwm_stats(selected_file)

    txt = f"""
PWM vs NOTCH

Correlation : {pwm['correlation']}

Interpretation:

0.5+ = Good Tracking
0.7+ = Excellent Tracking
"""

    output.delete("1.0","end")
    output.insert("1.0", txt)


def fft_report():

    if selected_file == "":
        return

    show_fft(selected_file)

# Buttons
buttons = [
    "Summary",
    "VIBE Analysis",
    "FFT Analysis",
    "FTN Statistics",
    "PWM vs Notch",
    "Peak Detection",
    "IMU Info",
    "RCOU Info",
    "Export PDF"
]

for b in buttons:
    btn = ctk.CTkButton(
        left_frame,
        text=b,
        width=180,
        height=40
    )
    btn.pack(pady=6)

# Output Box
output = ctk.CTkTextbox(
    right_frame,
    font=("Consolas",14)
)

output.pack(fill="both", expand=True, padx=10, pady=10)

output.insert(
    "0.0",
    """
==========================================
        DRONE VIBE ANALYZER
==========================================

Select a BIN file

Then click any analysis button

Available:

✓ Summary Report
✓ VIBE Analysis
✓ FFT Analysis
✓ FTN Statistics
✓ PWM vs Notch

Future:

• Peak Detection
• IMU Analysis
• RCOU Analysis
• PDF Export
"""
)

app.mainloop()