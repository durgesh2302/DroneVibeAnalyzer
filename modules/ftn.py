from pymavlink import mavutil
import pandas as pd

def get_ftn_stats(binfile):

    log = mavutil.mavlink_connection(binfile)

    data=[]

    while True:

        msg=log.recv_match(type='FTN',blocking=False)

        if msg is None:
            break

        data.append([
            msg.TimeUS,
            msg.I,
            msg.NF1
        ])

    df=pd.DataFrame(
        data,
        columns=["TimeUS","I","NF1"]
    )

    primary=df[df["I"]==0]

    return {
        "mean": round(primary["NF1"].mean(),2),
        "min": round(primary["NF1"].min(),2),
        "max": round(primary["NF1"].max(),2)
    }