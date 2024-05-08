

import threading as th

#################################
#     Communication parameter   #
#################################
# The server must be started before the client!
me = ['server']
# This is the name of the remote EV3 or PC we are connecting to.
SERVERID = 'ev3dev'
# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.
messages = ['occupied', 'gift4u']
send = [3] # 0 for occupied, 1 for gift4u, 3:send nothing.




thread2 = th.Thread(target=coms)


def main(thread2:th.Thread):
    if 'coms' in zoneSort and not thread2.is_alive:
        garbage = 'coms'
        thread2.start()

    return 0