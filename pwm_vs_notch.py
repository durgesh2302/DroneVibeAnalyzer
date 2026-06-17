from pymavlink import mavutil
import pandas as pd
import matplotlib.pyplot as plt

log = mavutil.mavlink_connection("flight.bin")

pwm=[]
nf=[]

while True:
    msg=log.recv_match(blocking=False)

    if msg is None:
        break

    if msg.get_type()=="RCOU":
        avg_pwm=(msg.C1+msg.C2+msg.C3+msg.C4+msg.C5+msg.C6)/6
        pwm.append(avg_pwm)

    elif msg.get_type()=="FTN" and msg.I==0:
        nf.append(msg.NF1)

n=min(len(pwm),len(nf))

pwm=pwm[:n]
nf=nf[:n]

corr=pd.Series(pwm).corr(pd.Series(nf))

print("Correlation =",corr)

plt.scatter(pwm,nf,s=1)
plt.xlabel("Average PWM")
plt.ylabel("Notch Frequency (Hz)")
plt.title("PWM vs Notch Frequency")
plt.grid()
plt.show()