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

    return {
        "mean_x": float(round(df["VibeX"].mean(),2)),
        "mean_y": float(round(df["VibeY"].mean(),2)),
        "mean_z": float(round(df["VibeZ"].mean(),2)),
        "max_z": float(round(df["VibeZ"].max(),2))
    }