from pymavlink import mavutil
import pandas as pd

log = mavutil.mavlink_connection("flight.bin")

data = []

while True:
    msg = log.recv_match(type='VIBE', blocking=False)

    if msg is None:
        break

    data.append([
        msg.TimeUS,
        msg.VibeX,
        msg.VibeY,
        msg.VibeZ
    ])

df = pd.DataFrame(
    data,
    columns=['TimeUS', 'VibeX', 'VibeY', 'VibeZ']
)

print(df.head())
print(df.describe())