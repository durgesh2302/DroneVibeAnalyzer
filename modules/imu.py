from pymavlink import mavutil
import pandas as pd

def get_imu_info(binfile):

    log = mavutil.mavlink_connection(binfile)

    gyro_x = []
    gyro_y = []
    gyro_z = []

    count = 0

    while True:

        msg = log.recv_match(type='IMU', blocking=False)

        if msg is None:
            break

        count += 1

        gyro_x.append(msg.GyrX)
        gyro_y.append(msg.GyrY)
        gyro_z.append(msg.GyrZ)

    return {
        "samples": count,
        "gx_mean": round(pd.Series(gyro_x).mean(), 2),
        "gy_mean": round(pd.Series(gyro_y).mean(), 2),
        "gz_mean": round(pd.Series(gyro_z).mean(), 2)
    }