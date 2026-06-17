from pymavlink import mavutil
import pandas as pd
import matplotlib.pyplot as plt

log = mavutil.mavlink_connection("flight.bin")

rcou=[]
ftn=[]

while True:
    msg=log.recv_match(blocking=False)

    if msg is None:
        break

    if msg.get_type()=="RCOU":
        rcou.append(msg.C1)

    elif msg.get_type()=="FTN" and msg.I==0:
        ftn.append(msg.NF1)

print("RCOU samples:",len(rcou))
print("FTN samples:",len(ftn))

plt.figure(figsize=(10,5))
plt.plot(ftn)
plt.title("Notch Frequency")
plt.show()