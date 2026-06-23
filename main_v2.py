import customtkinter as ctk
from tkinter import filedialog

from modules.peak import get_peaks
from modules.vibe import get_vibe_stats, show_vibe_graph
from modules.ftn import get_ftn_stats
from modules.pwm import get_pwm_stats
from modules.fft import show_fft
from modules.imu import get_imu_info
from modules.rcou import (
    get_rcou_info,
    show_rcou_graph,
    show_motor_stats_graph
)
from modules.health import get_health_score
from modules.assessment import get_assessment
from modules.pdf_export import export_pdf


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

    h = get_health_score(selected_file)

    report = f"""
==========================
DRONE HEALTH REPORT
==========================

Health Score : {h['overall']}/100

Vibration Status : HEALTHY

Mean X : {vibe['mean_x']}
Mean Y : {vibe['mean_y']}
Mean Z : {vibe['mean_z']}

Notch Mean : {ftn['mean']} Hz

PWM Correlation : {pwm['correlation']}

Recommendations

- Vibration acceptable
- Dynamic notch working
- No major resonance detected
"""

    output.delete("0.0","end")
    output.insert("0.0", report)

def health_report():

    if selected_file == "":
        return

    h = get_health_score(selected_file)

    report = f"""


==========================
HEALTH SCORE DASHBOARD
==========================

Overall Score : {h['overall']}/100

Status : {h['status']}

Vibration Score : {h['vibe_score']}/100
Motor Score     : {h['motor_score']}/100
FFT Score       : {h['fft_score']}/100
FTN Score       : {h['ftn_score']}/100
"""

    report += f"""
==========================
DETAILS
==========================

Max Vibration   : {h['max_vibration']}

Motor Difference: {h['balance_diff']}

Notch Span      : {h['notch_span']} Hz
"""


    output.delete("0.0", "end")
    output.insert("0.0", report)

def assessment_report():

    if selected_file == "":
        return

    a = get_assessment(selected_file)

    report = f"""
==========================
FLIGHT ASSESSMENT
==========================

Overall Score : {a['score']}/100

Status : {a['status']}

==========================
ISSUES
==========================
"""

    for issue in a["issues"]:
        report += f"\n- {issue}"

    report += "\n\n==========================\nRECOMMENDATIONS\n=========================="

    for rec in a["recommendations"]:
        report += f"\n- {rec}"

    output.delete("0.0", "end")
    output.insert("0.0", report)


def vibe_report():

    if selected_file == "":
        return

    vibe = get_vibe_stats(selected_file)

    report = f"""

==========================
VIBRATION ANALYSIS
==========================

VIBE X Mean : {vibe['mean_x']} m/s²

VIBE Y Mean : {vibe['mean_y']} m/s²

VIBE Z Mean : {vibe['mean_z']} m/s²

VIBE X Max : {vibe['max_x']} m/s²

VIBE Y Max : {vibe['max_y']} m/s²

VIBE Z Max : {vibe['max_z']} m/s²
"""

    if vibe["score"] >= 90:

        report += f"""

==========================
HEALTH ASSESSMENT
==========================

Vibration Score : {vibe['score']} / 100

Status : LOW VIBRATION

Recommendations:

- IMU isolation healthy

- Frame resonance not detected

- Propeller balance acceptable

- Flight controller vibration within limits
"""

    elif vibe["score"] >= 75:

        report += f"""

==========================
HEALTH ASSESSMENT
==========================

Vibration Score : {vibe['score']} / 100

Status : MODERATE VIBRATION

Recommendations:

- Check propeller balance

- Review motor output graph

- Inspect frame mounting

- Verify notch filtering
"""

    else:

        report += f"""

==========================
HEALTH ASSESSMENT
==========================

Vibration Score : {vibe['score']} / 100

Status : HIGH VIBRATION

Recommendations:

- Check propeller damage

- Inspect motor bearings

- Check frame resonance

- Review FFT peaks and notch tracking
"""

    output.delete("0.0", "end")
    output.insert("0.0", report)

def export_pdf_report():

    if selected_file == "":
        return

    filename = export_pdf(selected_file)

    output.delete("0.0", "end")
    output.insert(
        "0.0",
        f"PDF Generated Successfully\n\n{filename}"
    )

def vibe_graph():

    if selected_file == "":
        return

    show_vibe_graph(selected_file)


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

def imu_report():

    if selected_file == "":
        return

    imu = get_imu_info(selected_file)

    report = f"""
==========================
IMU INFORMATION
==========================

Total Samples : {imu['samples']}

Gyro X Mean : {imu['gx_mean']}

Gyro Y Mean : {imu['gy_mean']}

Gyro Z Mean : {imu['gz_mean']}

Status : HEALTHY

Recommendations:

✓ IMU data available

✓ Gyroscope logging detected

✓ Sensor operational
"""

    output.delete("0.0", "end")
    output.insert("0.0", report)

def rcou_graph():

    if selected_file == "":
        return

    show_rcou_graph(selected_file)

def rcou_graph():

    if selected_file == "":
        return

    show_rcou_graph(selected_file)


def motor_stats():

    if selected_file == "":
        return

    show_motor_stats_graph(selected_file)

def rcou_report():

    if selected_file == "":
        return

    rcou = get_rcou_info(selected_file)

    print(rcou)

    report = f"""
==========================
RCOU INFORMATION
==========================

Total Samples : {rcou['samples']}

Frame Type : {rcou['frame_type']}

Motor Count : {rcou['motor_count']}

PWM Min : {rcou['min']}

PWM Max : {rcou['max']}

PWM Mean : {rcou['mean']}

PWM Span : {rcou['span']}

==========================
INDIVIDUAL MOTOR ANALYSIS
==========================

Motor 1 Max : {rcou['m1_max']}

Motor 2 Max : {rcou['m2_max']}

Motor 3 Max : {rcou['m3_max']}

Motor 4 Max : {rcou['m4_max']}
"""

    if rcou["motor_count"] == 6:

        report += f"""

Motor 5 Max : {rcou['m5_max']}

Motor 6 Max : {rcou['m6_max']}
"""

    report += f"""

==========================
MOTOR BALANCE ANALYSIS
==========================

Motor 1 Avg : {rcou['m1_avg']}

Motor 2 Avg : {rcou['m2_avg']}

Motor 3 Avg : {rcou['m3_avg']}

Motor 4 Avg : {rcou['m4_avg']}
"""

    if rcou["motor_count"] == 6:

        report += f"""

Motor 5 Avg : {rcou['m5_avg']}

Motor 6 Avg : {rcou['m6_avg']}
"""

    if rcou["motor_count"] == 4:

        avgs = [
            rcou["m1_avg"],
            rcou["m2_avg"],
            rcou["m3_avg"],
            rcou["m4_avg"]
        ]

    else:

        avgs = [
            rcou["m1_avg"],
            rcou["m2_avg"],
            rcou["m3_avg"],
            rcou["m4_avg"],
            rcou["m5_avg"],
            rcou["m6_avg"]
        ]

    diff = round(max(avgs) - min(avgs), 2)

    report += f"""

Balance Difference : {diff}
"""

    if diff > 80:

        report += """

Status : IMBALANCED

Recommendations:

- Check CG balance

- Check propeller condition

- Check motor alignment

- Check frame twist
"""

    elif diff > 40:

        report += """

Status : MINOR IMBALANCE

Recommendations:

- Monitor future flights

- Compare motor outputs

- Check vibration report
"""

    else:

        report += """

Status : WELL BALANCED

Recommendations:

- Motor outputs healthy

- No major imbalance detected

- Frame balance looks good
"""

    report += """

==========================
FLIGHT ASSESSMENT
==========================
"""

    if rcou["span"] > 400:

        report += """

Status : AGGRESSIVE FLIGHT

- Large motor output variation

- Possible hard maneuvering

- Review VIBE report
"""

    elif rcou["span"] > 200:

        report += """

Status : NORMAL FLIGHT

- ESC outputs healthy

- Motor authority good

- PWM range acceptable
"""

    else:

        report += """

Status : LOW ACTIVITY

- Hover or light maneuvering

- ESC outputs stable

- Power system healthy
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
    text="Health Score",
    command=health_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Flight Assessment",
    command=assessment_report
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
    text="IMU Info",
    command=imu_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="RCOU Info",
    command=rcou_report
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Motor Graph",
    command=rcou_graph
).pack(pady=6)

motor_stats_btn = ctk.CTkButton(
    left_panel,
    text="Motor Stats",
    command=motor_stats
)

motor_stats_btn.pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Vibration Graph",
    command=vibe_graph
).pack(pady=6)

ctk.CTkButton(
    left_panel,
    text="Export PDF",
    command=export_pdf_report
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