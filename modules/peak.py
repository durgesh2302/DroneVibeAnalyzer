from pymavlink import mavutil
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

def get_peaks(binfile):

    log = mavutil.mavlink_connection(binfile)

    gyro = []

    while True:

        msg = log.recv_match(type='IMU', blocking=False)

        if msg is None:
            break

        gyro.append(msg.GyrZ)

    gyro = np.array(gyro)

    fs = 400
    N = len(gyro)

    yf = np.abs(fft(gyro))
    xf = fftfreq(N, 1/fs)

    mask = (xf > 20) & (xf < 200)

    xf = xf[mask]
    yf = yf[mask]

    peak_idx, _ = find_peaks(
        yf,
        distance=200,
        prominence=5
    )

    if len(peak_idx) == 0:
        return []

    amps = yf[peak_idx]

    best = peak_idx[np.argsort(amps)[-10:]]

    selected = []
    freq_used = []

    for i in reversed(best):

        freq = float(xf[i])

        keep = True

        for f in freq_used:

            if abs(freq - f) < 10:
                keep = False
                break

        if keep:
            selected.append(i)
            freq_used.append(freq)

        if len(selected) >= 5:
            break

    peaks = []

    for i in selected:

        peaks.append(
            (
                round(float(xf[i]), 2),
                round(float(yf[i]), 2)
            )
        )

    return peaks