from pymavlink import mavutil
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

log = mavutil.mavlink_connection("flight.bin")

gyro=[]

while True:
    msg=log.recv_match(type='IMU',blocking=False)

    if msg is None:
        break

    gyro.append(msg.GyrZ)

gyro=np.array(gyro)

fs=400
N=len(gyro)

yf=np.abs(fft(gyro))
xf=fftfreq(N,1/fs)

mask=(xf>20) & (xf<200)

freqs=xf[mask]
amps=yf[mask]

peaks,_=find_peaks(amps,height=np.max(amps)*0.01)

top=sorted(
    zip(freqs[peaks],amps[peaks]),
    key=lambda x:x[1],
    reverse=True
)[:10]

for f,a in top:
    print(f"Freq={f:.2f} Hz   Amp={a:.2f}")