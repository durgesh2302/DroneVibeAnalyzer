from pymavlink import mavutil
import pandas as pd

log = mavutil.mavlink_connection("flight.bin")

data=[]

while True:
    msg = log.recv_match(type='FTN', blocking=False)

    if msg is None:
        break

    data.append([
        msg.TimeUS,
        msg.I,
        msg.NF1
    ])

df = pd.DataFrame(data, columns=["TimeUS","I","NF1"])

print(df.groupby("I")["NF1"].describe())