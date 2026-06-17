from pymavlink import mavutil

log = mavutil.mavlink_connection("flight.bin")

while True:
    msg = log.recv_match(type='IMU', blocking=False)

    if msg is None:
        continue

    print(msg)
    break