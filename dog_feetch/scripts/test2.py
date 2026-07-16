import time
import numpy as np
import rustypot  #  (Feetech)  ( Rust  Python )
usb_port = "/dev/ttyACM0"
io = rustypot.feetech(usb_port, 1000000)



joints = {
    # "right_front_hip_joint": 6,
    # "right_front_knee_joint": 7,
    # "right_front_ankle_joint": 8,

    # "left_front_hip_joint": 0,
    # "left_front_knee_joint": 4,   # ID 4
    # "left_front_ankle_joint": 5,  # ID 5

    "right_back_hip_joint": 9,    # ID 9
    "right_back_knee_joint": 10,  # ID 10
    "right_back_ankle_joint": 11, # ID 11

    "left_back_hip_joint": 3,
    "left_back_knee_joint": 1,    # ID 1
    "left_back_ankle_joint": 2,   # ID 2
}


def set_kps():
    global io
    """This script is a local hardware test entry point."""
    kps = 10
    io.set_kps([1], [10])

#set_kps()
while True:
    io.write_goal_position([0,1,2,3,4,5,6,7,8,9,10,11], [0,0,0,0,0,0,0,0,0,0,0,0])
    time.sleep(0.1)
