from pymavlink import mavutil

log = mavutil.mavlink_connection("flight.bin")

while True:
    msg = log.recv_match(blocking=False)

    if msg is None:
        break

    print(msg.get_type())