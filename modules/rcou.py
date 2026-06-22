from pymavlink import mavutil
import pandas as pd

def get_rcou_info(binfile):

    log = mavutil.mavlink_connection(binfile)

    pwm = []

    while True:

        msg = log.recv_match(type='RCOU', blocking=False)

        if msg is None:
            break

        avg_pwm = (
            msg.C1 +
            msg.C2 +
            msg.C3 +
            msg.C4 +
            msg.C5 +
            msg.C6
        ) / 6

        pwm.append(avg_pwm)

    s = pd.Series(pwm)

    return {
        "samples": len(pwm),
        "min": round(float(s.min()), 2),
        "max": round(float(s.max()), 2),
        "mean": round(float(s.mean()), 2)
    }