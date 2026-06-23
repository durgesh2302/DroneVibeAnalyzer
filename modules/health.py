from modules.vibe import get_vibe_stats
from modules.rcou import get_rcou_info
from modules.ftn import get_ftn_stats
from modules.peak import get_peaks


def get_health_score(logfile):

    vibe = get_vibe_stats(logfile)
    rcou = get_rcou_info(logfile)
    ftn = get_ftn_stats(logfile)
    peaks = get_peaks(logfile)

    # =====================================
    # VIBRATION SCORE
    # =====================================

    max_vibe = max(
        vibe["mean_x"],
        vibe["mean_y"],
        vibe["mean_z"]
    )

    if max_vibe <= 3:
        vibe_score = 100
    elif max_vibe <= 5:
        vibe_score = 95
    elif max_vibe <= 10:
        vibe_score = 90
    elif max_vibe <= 15:
        vibe_score = 75
    elif max_vibe <= 20:
        vibe_score = 60
    else:
        vibe_score = 40

    # =====================================
    # MOTOR BALANCE SCORE
    # =====================================

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

    diff = max(avgs) - min(avgs)

    if diff <= 20:
        motor_score = 100
    elif diff <= 40:
        motor_score = 90
    elif diff <= 80:
        motor_score = 75
    elif diff <= 120:
        motor_score = 60
    else:
        motor_score = 40

    # =====================================
    # FFT / RESONANCE SCORE
    # =====================================

    if len(peaks) == 0:

        fft_score = 100

    else:

        strongest_peak = peaks[0][1]

        if strongest_peak <= 3:
            fft_score = 100
        elif strongest_peak <= 5:
            fft_score = 90
        elif strongest_peak <= 10:
            fft_score = 80
        elif strongest_peak <= 20:
            fft_score = 65
        else:
            fft_score = 50

    # =====================================
    # FTN SCORE
    # =====================================

    notch_span = ftn["max"] - ftn["min"]

    if notch_span >= 80:
        ftn_score = 100
    elif notch_span >= 50:
        ftn_score = 95
    elif notch_span >= 30:
        ftn_score = 85
    elif notch_span >= 15:
        ftn_score = 75
    else:
        ftn_score = 60

    # =====================================
    # OVERALL SCORE
    # =====================================

    overall = round(
        (
            vibe_score * 0.35 +
            motor_score * 0.25 +
            fft_score * 0.25 +
            ftn_score * 0.15
        )
    )

    if overall >= 90:
        status = "EXCELLENT"

    elif overall >= 80:
        status = "HEALTHY"

    elif overall >= 65:
        status = "WARNING"

    else:
        status = "CRITICAL"

    return {
        "overall": overall,
        "status": status,
        "vibe_score": vibe_score,
        "motor_score": motor_score,
        "fft_score": fft_score,
        "ftn_score": ftn_score,
        "balance_diff": round(diff, 2),
        "max_vibration": round(max_vibe, 2),
        "notch_span": round(notch_span, 2)
    }