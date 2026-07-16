#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOG_ROOT = os.path.dirname(SCRIPT_DIR)
if DOG_ROOT not in sys.path:
    sys.path.insert(0, DOG_ROOT)

from runtime.position_hwi import HWI

def main():
    hwi = HWI(usb_port="/dev/ttyACM0")
    hwi.turn_off()#####
    time.sleep(0.3)
    print("")
    input()

    pos_arr = None
    max_retry = 3
    for i in range(max_retry):
        pos_arr = hwi.get_present_positions()
        if pos_arr is not None:
            break
        print(f"{i+1}0.2s...")
        time.sleep(0.2)

    if pos_arr is None:
        print("")
        sys.exit(1)

    joint_list = list(hwi.joints.keys())
    res = dict(zip(joint_list, pos_arr))

    print("\ninit_pos")
    print(f'"right_front_hip_joint": {res["right_front_hip_joint"]:.6f},')
    print(f'"right_front_knee_joint": {res["right_front_knee_joint"]:.6f},')
    print(f'"right_front_ankle_joint": {res["right_front_ankle_joint"]:.6f},')
    print(f'"left_front_hip_joint": {res["left_front_hip_joint"]:.6f},')
    print(f'"left_front_knee_joint": {res["left_front_knee_joint"]:.6f},')
    print(f'"left_front_ankle_joint": {res["left_front_ankle_joint"]:.6f},')
    print(f'"right_back_hip_joint": {res["right_back_hip_joint"]:.6f},')
    print(f'"right_back_knee_joint": {res["right_back_knee_joint"]:.6f},')
    print(f'"right_back_ankle_joint": {res["right_back_ankle_joint"]:.6f},')
    print(f'"left_back_hip_joint": {res["left_back_hip_joint"]:.6f},')
    print(f'"left_back_knee_joint": {res["left_back_knee_joint"]:.6f},')
    print(f'"left_back_ankle_joint": {res["left_back_ankle_joint"]:.6f},')

if __name__ == "__main__":
    main()
