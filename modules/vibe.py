from pymavlink import mavutil
import pandas as pd

def get_vibe_stats(binfile):

    log = mavutil.mavlink_connection(binfile)

    data=[]

    while True:

        msg=log.recv_match(type='VIBE',blocking=False)

        if msg is None:
            break

        data.append([
            msg.TimeUS,
            msg.VibeX,
            msg.VibeY,
            msg.VibeZ
        ])

    df=pd.DataFrame(
        data,
        columns=["TimeUS","VibeX","VibeY","VibeZ"]
    )

    score = 100 - (
        df["VibeX"].mean() +
        df["VibeY"].mean() +
        df["VibeZ"].mean()
    )

    score = max(0, round(score,1))

    return {

        "mean_x": round(float(df["VibeX"].mean()),2),
        "mean_y": round(float(df["VibeY"].mean()),2),
        "mean_z": round(float(df["VibeZ"].mean()),2),

        "max_x": round(float(df["VibeX"].max()),2),
        "max_y": round(float(df["VibeY"].max()),2),
        "max_z": round(float(df["VibeZ"].max()),2),

        "score": score
    }

import matplotlib.pyplot as plt

def show_vibe_graph(binfile):

    log = mavutil.mavlink_connection(binfile)

    vx = []
    vy = []
    vz = []

    while True:

        msg = log.recv_match(type='VIBE', blocking=False)

        if msg is None:
            break

        vx.append(msg.VibeX)
        vy.append(msg.VibeY)
        vz.append(msg.VibeZ)

    plt.figure(figsize=(12,6))

    plt.plot(vx, label="VIBE X")
    plt.plot(vy, label="VIBE Y")
    plt.plot(vz, label="VIBE Z")

    plt.title("Vibration Analysis")

    plt.xlabel("Sample Number")

    plt.ylabel("Vibration (m/s²)")

    plt.grid(True)

    plt.legend()

    plt.show()