from pymavlink import mavutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

log = mavutil.mavlink_connection("flight.bin")

gyro = []

while True:
    msg = log.recv_match(type='IMU', blocking=False)

    if msg is None:
        break

    gyro.append(msg.GyrZ)

gyro = np.array(gyro)

N = len(gyro)

# IMU output rate ~400 Hz (AHz≈398)
fs = 400

yf = np.abs(fft(gyro))
xf = fftfreq(N, 1/fs)

positive = xf > 0

plt.figure(figsize=(10,5))
plt.plot(xf[positive], yf[positive])
plt.xlim(0,200)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Gyro FFT Spectrum")
plt.grid()
plt.show()

peak_freq = xf[np.argmax(yf[positive])]
print("Peak Frequency =", peak_freq)