from pymavlink import mavutil
import pandas as pd
import numpy as np

def get_rcou_info(binfile):

    log = mavutil.mavlink_connection(binfile)

    m1=[]
    m2=[]
    m3=[]
    m4=[]
    m5=[]
    m6=[]

    pwm=[]

    while True:

        msg = log.recv_match(type='RCOU', blocking=False)

        if msg is None:
            break

        m1.append(msg.C1)
        m2.append(msg.C2)
        m3.append(msg.C3)
        m4.append(msg.C4)
        m5.append(msg.C5)
        m6.append(msg.C6)

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

    frame_type = "QUAD"
    motor_count = 4

    if max(m5) > 10 or max(m6) > 10:
        frame_type = "HEXA"
        motor_count = 6

    return {
        "samples": len(pwm),

        "min": round(float(s.min()), 2),
        "max": round(float(s.max()), 2),
        "mean": round(float(s.mean()), 2),
        "span": round(float(s.max() - s.min()), 2),

        "frame_type": frame_type,
        "motor_count": motor_count,

        "m1_max": max(m1),
        "m2_max": max(m2),
        "m3_max": max(m3),
        "m4_max": max(m4),
        "m5_max": max(m5),
        "m6_max": max(m6),

	"m1_avg": round(sum(m1)/len(m1), 2),
	"m2_avg": round(sum(m2)/len(m2), 2),
	"m3_avg": round(sum(m3)/len(m3), 2),
	"m4_avg": round(sum(m4)/len(m4), 2),
	"m5_avg": round(sum(m5)/len(m5), 2),
	"m6_avg": round(sum(m6)/len(m6), 2),

	"m1_std": round(float(np.std(m1)), 2),
	"m2_std": round(float(np.std(m2)), 2),
	"m3_std": round(float(np.std(m3)), 2),
	"m4_std": round(float(np.std(m4)), 2),
	"m5_std": round(float(np.std(m5)), 2),
	"m6_std": round(float(np.std(m6)), 2),
    }


import matplotlib.pyplot as plt
from pymavlink import mavutil

def show_rcou_graph(binfile):



    log = mavutil.mavlink_connection(binfile)

    m1=[]
    m2=[]
    m3=[]
    m4=[]
    m5=[]
    m6=[]

    while True:

        msg = log.recv_match(type='RCOU', blocking=False)

        if msg is None:
            break

        m1.append(msg.C1)
        m2.append(msg.C2)
        m3.append(msg.C3)
        m4.append(msg.C4)
        m5.append(msg.C5)
        m6.append(msg.C6)

    plt.figure(figsize=(12,6))

    plt.plot(m1, label="Motor 1")
    plt.plot(m2, label="Motor 2")
    plt.plot(m3, label="Motor 3")
    plt.plot(m4, label="Motor 4")

    if max(m5) > 10:
        plt.plot(m5, label="Motor 5")

    if max(m6) > 10:
        plt.plot(m6, label="Motor 6")

    plt.title("Motor PWM Output")

    plt.xlabel("Sample")

    plt.ylabel("PWM")

    plt.grid(True)

    plt.legend()

    plt.show()

def show_motor_stats_graph(binfile):

    data = get_rcou_info(binfile)

    motors = ["M1", "M2", "M3", "M4"]

    avg = [
        data["m1_avg"],
        data["m2_avg"],
        data["m3_avg"],
        data["m4_avg"]
    ]

    mx = [
        data["m1_max"],
        data["m2_max"],
        data["m3_max"],
        data["m4_max"]
    ]

    std = [
        data["m1_std"],
        data["m2_std"],
        data["m3_std"],
        data["m4_std"]
    ]

    if data["motor_count"] == 6:

        motors.extend(["M5","M6"])

        avg.extend([
            data["m5_avg"],
            data["m6_avg"]
        ])

        mx.extend([
            data["m5_max"],
            data["m6_max"]
        ])

        std.extend([
            data["m5_std"],
            data["m6_std"]
        ])

    import numpy as np
    import matplotlib.pyplot as plt

    x = np.arange(len(motors))
    w = 0.25

    plt.figure(figsize=(10,6))

    plt.bar(x-w, avg, width=w, label="Average PWM")
    plt.bar(x, mx, width=w, label="Max PWM")
    plt.bar(x+w, std, width=w, label="Variation")

    plt.xticks(x, motors)

    plt.ylabel("Value")

    plt.title("Motor Statistics")

    plt.legend()

    plt.grid(True)

    plt.show()