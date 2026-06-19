from pymavlink import mavutil
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def show_fft(binfile):

    log = mavutil.mavlink_connection(binfile)

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

    mask=(xf>0)&(xf<200)

    plt.figure(figsize=(10,5))
    plt.plot(xf[mask],yf[mask])

    plt.title("Gyro FFT Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()