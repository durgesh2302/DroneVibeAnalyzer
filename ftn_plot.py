from pymavlink import mavutil
import pandas as pd
import matplotlib.pyplot as plt

log = mavutil.mavlink_connection("flight.bin")

data=[]

while True:
    msg=log.recv_match(type='FTN',blocking=False)

    if msg is None:
        break

    if msg.I==0:
        data.append(msg.NF1)

plt.plot(data)
plt.title("Primary Notch Frequency")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Sample")
plt.grid()
plt.show()

print("Min :", min(data))
print("Max :", max(data))
print("Avg :", sum(data)/len(data))