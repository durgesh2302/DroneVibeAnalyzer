from pymavlink import mavutil

log = mavutil.mavlink_connection("flight.bin")

msg_types = set()

while True:
    msg = log.recv_match(blocking=False)

    if msg is None:
        break

    msg_types.add(msg.get_type())

for m in sorted(msg_types):
    print(m)