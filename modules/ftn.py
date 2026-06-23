from pymavlink import mavutil
import pandas as pd

def get_ftn_stats(binfile):

    log = mavutil.mavlink_connection(binfile)

    data = []

    while True:

        msg = log.recv_match(type='FTN', blocking=False)

        if msg is None:
            break

        data.append([
            msg.TimeUS,
            msg.I,
            msg.NF1
        ])

    if len(data) == 0:

        return {
            "mean": 0,
            "min": 0,
            "max": 0
        }

    df = pd.DataFrame(
        data,
        columns=["TimeUS", "I", "NF1"]
    )

    primary = df[df["I"] == 0]

    if len(primary) == 0:

        return {
            "mean": 0,
            "min": 0,
            "max": 0
        }

    return {
        "mean": round(float(primary["NF1"].mean()), 2),
        "min": round(float(primary["NF1"].min()), 2),
        "max": round(float(primary["NF1"].max()), 2)
    }