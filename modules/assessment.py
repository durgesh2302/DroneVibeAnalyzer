from modules.health import get_health_score


def get_assessment(logfile):

    h = get_health_score(logfile)

    issues = []
    recommendations = []

    # Vibration
    if h["vibe_score"] < 80:
        issues.append("High vibration detected")
        recommendations.append("Check propeller balance")
        recommendations.append("Inspect frame mounting")

    # Motor Balance
    if h["motor_score"] < 80:
        issues.append("Motor imbalance detected")
        recommendations.append("Review motor outputs")
        recommendations.append("Check motor bearings")

    # FFT
    if h["fft_score"] < 80:
        issues.append("Resonance peak detected")
        recommendations.append("Review FFT analysis")
        recommendations.append("Verify harmonic notch settings")

    # FTN
    if h["ftn_score"] < 80:
        issues.append("Weak notch tracking")
        recommendations.append("Verify dynamic notch configuration")

    if len(issues) == 0:
        issues.append("No significant issues detected")
        recommendations.append("System operating normally")

    return {
        "score": h["overall"],
        "status": h["status"],
        "issues": issues,
        "recommendations": recommendations
    }