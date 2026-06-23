from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from modules.health import get_health_score
from modules.vibe import get_vibe_stats
from modules.ftn import get_ftn_stats
from modules.rcou import get_rcou_info
from modules.imu import get_imu_info
from modules.peak import get_peaks
from modules.assessment import get_assessment


def export_pdf(logfile):

    pdf = SimpleDocTemplate("DroneVibe_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    h = get_health_score(logfile)
    vibe = get_vibe_stats(logfile)
    ftn = get_ftn_stats(logfile)
    rcou = get_rcou_info(logfile)
    imu = get_imu_info(logfile)
    peaks = get_peaks(logfile)
    assessment = get_assessment(logfile)

    # ====================================
    # TITLE
    # ====================================

    story.append(
        Paragraph(
            "DroneVibeAnalyzer Engineering Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # ====================================
    # HEALTH SCORE
    # ====================================

    story.append(
        Paragraph("Health Dashboard", styles["Heading1"])
    )

    story.append(
        Paragraph(
            f"Overall Score : {h['overall']}/100",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Status : {h['status']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Vibration Score : {h['vibe_score']}/100",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Motor Score : {h['motor_score']}/100",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"FFT Score : {h['fft_score']}/100",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"FTN Score : {h['ftn_score']}/100",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ====================================
    # FLIGHT ASSESSMENT
    # ====================================

    story.append(
        Paragraph("Flight Assessment", styles["Heading1"])
    )

    for issue in assessment["issues"]:

        story.append(
            Paragraph(
                f"Issue : {issue}",
                styles["Normal"]
            )
        )

    for rec in assessment["recommendations"]:

        story.append(
            Paragraph(
                f"Recommendation : {rec}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # ====================================
    # VIBRATION
    # ====================================

    story.append(
        Paragraph("Vibration Analysis", styles["Heading1"])
    )

    story.append(
        Paragraph(
            f"Mean X : {vibe['mean_x']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Mean Y : {vibe['mean_y']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Mean Z : {vibe['mean_z']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Max X : {vibe['max_x']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Max Y : {vibe['max_y']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Max Z : {vibe['max_z']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ====================================
    # FFT PEAKS
    # ====================================

    story.append(
        Paragraph("FFT Peak Detection", styles["Heading1"])
    )

    for i, peak in enumerate(peaks[:5], start=1):

        story.append(
            Paragraph(
                f"Peak {i} : {peak[0]:.2f} Hz | Amplitude : {peak[1]:.2f}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # ====================================
    # FTN
    # ====================================

    story.append(
        Paragraph("FTN Statistics", styles["Heading1"])
    )

    story.append(
        Paragraph(
            f"Mean NF1 : {ftn['mean']} Hz",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Min NF1 : {ftn['min']} Hz",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Max NF1 : {ftn['max']} Hz",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ====================================
    # IMU
    # ====================================

    story.append(
        Paragraph("IMU Information", styles["Heading1"])
    )

    for key, value in imu.items():

        story.append(
            Paragraph(
                f"{key} : {value}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # ====================================
    # RCOU
    # ====================================

    story.append(
        Paragraph("RCOU Information", styles["Heading1"])
    )

    for key, value in rcou.items():

        story.append(
            Paragraph(
                f"{key} : {value}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    pdf.build(story)

    return "DroneVibe_Report.pdf"