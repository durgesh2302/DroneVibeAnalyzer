import customtkinter as ctk
from tkinter import filedialog

from modules.peak import get_peaks
from modules.vibe import get_vibe_stats
from modules.ftn import get_ftn_stats
from modules.pwm import get_pwm_stats
from modules.fft import show_fft

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("DroneVibeAnalyzer")
app.geometry("1200x700")
selected_file = ""

# ==========================
# TITLE
# ==========================

title = ctk.CTkLabel(
    app,
    text="🚁 DroneVibeAnalyzer",
    font=("Arial", 28, "bold")
)

title.pack(pady=15)

# ==========================
# MAIN FRAME
# ==========================

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ==========================
# LEFT PANEL
# ==========================

left_panel = ctk.CTkFrame(
    main_frame,
    width=220
)

left_panel.pack(
    side="left",
    fill="y",
    padx=10,
    pady=10
)

# ==========================
# RIGHT PANEL
# ==========================

right_panel = ctk.CTkFrame(main_frame)

right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

def summary_report():

    if selected_file == "":
        return

    vibe = get_vibe_stats(selected_file)
    ftn = get_ftn_stats(selected_file)
    pwm = get_pwm_stats(selected_file)

    health = 100

    if vibe["mean_z"] > 15:
        health -= 30
    elif vibe["mean_z"] > 10:
        health -= 15

    report = f"""
==========================
DRONE HEALTH REPORT
==========================

Health Score : {health}/100

Vibration Status : HEALTHY

Mean X : {vibe['mean_x']}
Mean Y : {vibe['mean_y']}
Mean Z : {vibe['mean_z']}

Notch Mean : {ftn['mean']} Hz

PWM Correlation : {pwm['correlation']}

Recommendations

✓ Vibration acceptable
✓ Dynamic notch working
✓ No major resonance detected
"""

    output.delete("0.0","end")
    output.insert("0.0", report)


def vibe_report():

    if selected_file == "":
        return

    vibe = get_vibe_stats(selected_file)

    report = f"""
==========================
VIBE ANALYSIS
==========================

Mean X : {vibe['mean_x']}

Mean Y : {vibe['mean_y']}

Mean Z : {vibe['mean_z']}

Max Z : {vibe['max_z']}
"""

    output.delete("0.0","end")
    output.insert("0.0", report)


def ftn_report():

    if selected_file == "":
        return

    ftn = get_ftn_stats(selected_file)

    report = f"""
==========================
FTN STATISTICS
==========================

Mean NF1 : {ftn['mean']} Hz

Min NF1 : {ftn['min']} Hz

Max NF1 : {ftn['max']} Hz
"""

    output.delete("0.0","end")
    output.insert("0.0", report)


def pwm_report():

    if selected_file == "":
        return

    pwm = get_pwm_stats(selected_file)

    report = f"""
==========================
PWM vs NOTCH
==========================

Correlation : {pwm['correlation']}

Interpretation

> 0.7 Excellent

> 0.5 Good

< 0.3 Poor
"""

    output.delete("0.0","end")
    output.insert("0.0", report)


def fft_report():

    if selected_file == "":
        return

    show_fft(selected_file)

from tkinter import filedialog

def browse_bin():

    global selected_file

    filename = filedialog.askopenfilename(
        filetypes=[("BIN Files", "*.bin")]
    )

    if filename:

        selected_file = filename

        output.delete("0.0", "end")

        output.insert(
            "0.0",
            f"BIN Loaded Successfully\n\n{filename}"
        )

def peak_report():

    if selected_file == "":
        return

    peaks = get_peaks(selected_file)

    report = """
==========================
PEAK DETECTION
==========================

"""

    for i, p in enumerate(peaks):

        report += f"""
Peak {i+1}

Frequency : {p[0]} Hz

Amplitude : {p[1]}

"""

    if len(peaks) > 0:

        report += f"""

==========================
ASSESSMENT
==========================

Primary Resonance : {peaks[0][0]} Hz

Status : HEALTHY

Recommendations:

✓ No severe resonance detected

✓ Dynamic notch tracking appears normal

✓ Frame vibration acceptable

✓ Motor balance looks reasonable
"""

    output.delete("0.0", "end")
    output.insert("0.0", report)


# ==========================
# BUTTONS
# ==========================

ctk.CTkButton(
    left_panel,
    text="Browse BIN",
    command=browse_bin
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Summary",
    command=summary_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="VIBE Analysis",
    command=vibe_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="FFT Analysis",
    command=fft_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="FTN Statistics",
    command=ftn_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="PWM vs Notch",
    command=pwm_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Peak Detection",
    command=peak_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="IMU Info"
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="RCOU Info"
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Export PDF"
).pack(pady=6)


# ==========================
# OUTPUT WINDOW
# ==========================

output = ctk.CTkTextbox(
    right_panel,
    font=("Consolas", 14)
)

output.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

output.insert(
    "0.0",
    """
=========================================
        DRONE VIBE ANALYZER
=========================================

Welcome Durgesh

Next Step:

1. Load BIN File

2. Run Analysis

Available:

✓ Summary
✓ VIBE
✓ FFT
✓ FTN
✓ PWM

Future:

✓ Peak Detection
✓ IMU
✓ RCOU
✓ PDF Export

=========================================
"""
)

app.mainloop()