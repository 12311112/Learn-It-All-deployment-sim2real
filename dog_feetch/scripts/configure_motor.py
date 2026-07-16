#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pypot.feetech import FeetechSTS3215IO
import argparse
import time
# This script configures Feetech servo parameters.

DEFAULT_ID = 1  #  ID  1

# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
parser = argparse.ArgumentParser(description=" STS3215  ID ")
parser.add_argument(
    "--port",
    help=" /dev/ttyUSB0 Linux  `ls /dev/tty* | grep usb` ",
    default="/dev/ttyACM0",
)
parser.add_argument(
    "--id",
    help=" ID",
    type=str,
    required=True
)
args = parser.parse_args()

# This script configures Feetech servo parameters.
io = FeetechSTS3215IO(args.port)
current_id = DEFAULT_ID


def scan():
    """
    This script configures Feetech servo parameters.
    This script configures Feetech servo parameters.
    """
    found_id = None
    for i in range(255):
        print(f" ID {i} ...")
        try:
            # This script configures Feetech servo parameters.
            io.get_present_position([i])
            found_id = i
            print(f" ID : {found_id}")
            break
        except Exception:
            # This script configures Feetech servo parameters.
            pass
    return found_id


# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
try:
    # This script configures Feetech servo parameters.
    io.get_present_position([DEFAULT_ID])
except Exception:
    # This script configures Feetech servo parameters.
    print(f" ID ({DEFAULT_ID})  ...")
    res = scan()
    if res is not None:
        current_id = res
    else:
        print(" ...")
        exit()


# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
kp = io.get_P_coefficient([current_id])
ki = io.get_I_coefficient([current_id])
kd = io.get_D_coefficient([current_id])
max_acceleration = io.get_maximum_acceleration([current_id])
acceleration = io.get_acceleration([current_id])
mode = io.get_mode([current_id])


# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
io.set_lock({current_id: 0})                #  EEPROM
io.set_mode({current_id: 0})                # 0
io.set_maximum_acceleration({current_id: 0}) #  0
io.set_acceleration({current_id: 0})         #  0

# This script configures Feetech servo parameters.
io.set_P_coefficient({current_id: 32})
io.set_I_coefficient({current_id: 0})
io.set_D_coefficient({current_id: 0})

# This script configures Feetech servo parameters.
io.change_id({current_id: int(args.id)})
current_id = int(args.id) #  ID

time.sleep(1) #  1  ID  EEPROM

# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
# This script configures Feetech servo parameters.
io.set_goal_position({current_id: 0})
time.sleep(1)

# ==========================================
# This script configures Feetech servo parameters.
# ==========================================
print("======  ======")
print(f" ID   : {current_id}")
print(f" (P)   : {io.get_P_coefficient([current_id])}")
print(f" (I)   : {io.get_I_coefficient([current_id])}")
print(f" (D)   : {io.get_D_coefficient([current_id])}")
print(f"     : {io.get_acceleration([current_id])}")
print(f" : {io.get_maximum_acceleration([current_id])}")
print(f"   : {io.get_mode([current_id])} (0 )")
print("======================")
