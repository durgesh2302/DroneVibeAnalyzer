# 🚁 DroneVibeAnalyzer

Python-based ArduPilot BIN log analysis toolkit.

## Features

* VIBE (vibration) analysis
* FFT spectrum extraction from IMU data
* Harmonic frequency detection
* Harmonic notch filter validation
* Motor RPM estimation from vibration frequencies
* PWM vs Notch Frequency correlation

## Example Results

* Dominant vibration frequency: ~62–68 Hz
* Second harmonic: ~133 Hz
* Harmonic notch tracking range: 65–80 Hz
* Estimated motor RPM: 3900–4800 RPM
* Vibration levels: Healthy

## Installation

```bash
pip install -r requirements.txt
```

## Scripts

* `read_log.py` – Read ArduPilot BIN logs
* `vibe_analysis.py` – Vibration analysis
* `gyro_fft.py` – FFT spectrum generation
* `peak_detect.py` – Dominant frequency detection
* `ftn_stats.py` – Harmonic notch statistics
* `ftn_plot.py` – Notch frequency visualization
* `pwm_vs_notch.py` – PWM vs notch correlation

## Future Improvements

* PDF report generation
* GUI dashboard
* PID tuning analysis
* Automatic notch recommendations
