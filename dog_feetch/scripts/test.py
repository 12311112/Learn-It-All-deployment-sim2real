#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from runtime.position_hwi import HWI

# This script is a local hardware test entry point.
TEST_DELTA_DEG = 8.0
TEST_DELTA_REL = np.deg2rad(TEST_DELTA_DEG)
SERIAL_PORT = "/dev/ttyACM0"
# ===================================================

JOINT_DIRECTION_DESC = {
    "right_front_hip_joint":   " = ",
    "right_front_knee_joint":  " = ",
    "right_front_ankle_joint": " = ",
    "left_front_hip_joint":    " = ",
    "left_front_knee_joint":   " = ",
    "left_front_ankle_joint":  " = ",
    "right_back_hip_joint":    " = ",
    "right_back_knee_joint":   " = ",
    "right_back_ankle_joint":  " = ",
    "left_back_hip_joint":     " = ",
    "left_back_knee_joint":    " = ",
    "left_back_ankle_joint":   " = ",
}

def main():
    print("=" * 70)
    print(" | ")
    print(f"{TEST_DELTA_DEG} ({np.round(TEST_DELTA_REL, 4)} rad)")
    print("  Ctrl+C ")
    print("=" * 70)

    # This script is a local hardware test entry point.
    hwi = HWI(SERIAL_PORT)
    joint_names = list(hwi.joints.keys())
    init_pos = hwi.init_pos
    signs = hwi.real_pose_signs_rl

    print(f"\n {len(joint_names)} ")
    for i, name in enumerate(joint_names):
        print(f"  [{i:2d}] {name:30s} sign = {signs[name]:.0f}")

    # This script is a local hardware test entry point.
    print("\n...")
    hwi.turn_on()
    print(" \n")

    try:
        for idx, joint_name in enumerate(joint_names):
            input(f"\n>>>  [{idx}] {joint_name}")

            print("-" * 50)
            print(f"{joint_name}")
            print(f" sign = {signs[joint_name]}")
            print(f"{JOINT_DIRECTION_DESC[joint_name]}")

            # This script is a local hardware test entry point.
            pos_before = hwi.get_present_positions()
            if pos_before is None:
                print(" ")
                break
            print(f": {np.round(pos_before[idx], 4)} rad ({np.round(np.rad2deg(pos_before[idx]), 2)})")

            # This script is a local hardware test entry point.
            target_dict = init_pos.copy()
            target_dict[joint_name] = init_pos[joint_name] + TEST_DELTA_REL * signs[joint_name]
            hwi.set_position_all(target_dict)
            time.sleep(0.6)

            # This script is a local hardware test entry point.
            pos_after = hwi.get_present_positions()
            if pos_after is None:
                print(" ")
                break
            print(f": {np.round(pos_after[idx], 4)} rad ({np.round(np.rad2deg(pos_after[idx]), 2)})")
            delta_actual = pos_after[idx] - pos_before[idx]
            print(f": {np.round(np.rad2deg(delta_actual), 2)} ")

            if abs(delta_actual) < 0.005:
                print("  ID")

            print(" ")
            input("")

            # This script is a local hardware test entry point.
            hwi.set_position_all(init_pos)
            time.sleep(0.5)
            print(" ")

        print("\n" + "=" * 70)
        print(" 12")
        print(" position_hwi.py  sign ")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n\n  ")
    finally:
        print("\n...")
        try:
            hwi.turn_off()
            print(" ")
        except Exception as e:
            print(f"{e}")

if __name__ == "__main__":
    main()
