#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script checks servo direction mapping.
======================
This script checks servo direction mapping.
  This script checks servo direction mapping.
  This script checks servo direction mapping.
     This script checks servo direction mapping.
  This script checks servo direction mapping.
     This script checks servo direction mapping.
     This script checks servo direction mapping.

This script checks servo direction mapping.
  python test_servo_direction.py [--usb-port /dev/ttyUSB0] [--angle 3] [--kp 15]
"""

import argparse
import math
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from runtime.position_hwi import HWI


def deg2rad(deg):
    return deg * math.pi / 180.0


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--usb-port",
        default="/dev/ttyUSB0",
        help=" /dev/ttyUSB0",
    )
    parser.add_argument(
        "--angle",
        type=float,
        default=5.0,
        help=" 3",
    )
    args = parser.parse_args()

    delta_rad = deg2rad(args.angle)

    # This script checks servo direction mapping.
    print(f"[INFO] : {args.usb_port}")
    hwi = HWI(usb_port=args.usb_port)

    # This script checks servo direction mapping.
    id_to_name = {v: k for k, v in hwi.joints.items()}
    sorted_ids = sorted(id_to_name.keys())  # [0, 1, 2, ..., 11]

    # This script checks servo direction mapping.
    # This script checks servo direction mapping.
    print("[INFO]  turn_on ...")
    hwi.turn_on()
    print("[INFO]  init_pos\n")

    # This script checks servo direction mapping.
    print("=" * 60)
    print(f"     init_pos  +{args.angle}")
    print(f"   {len(sorted_ids)}  ID 011 ")
    print("=" * 60)
    print("  ")
    print("    Enter  'r' = ")
    print("    'n'          = ")
    print("    'q'          = ")
    print("=" * 60 + "\n")

    for servo_id in sorted_ids:
        joint_name = id_to_name[servo_id]
        init_value = hwi.init_pos[joint_name]

        print(f">>> [{servo_id:2d}] {joint_name}")
        print(f"    init_pos = {init_value:.6f} rad ({math.degrees(init_value):.2f})")
        print(f"     = {init_value + delta_rad:.6f} rad ({math.degrees(init_value + delta_rad):.2f})")

        # This script checks servo direction mapping.
        _do_test(hwi, joint_name, servo_id, init_value, delta_rad)

        # This script checks servo direction mapping.
        while True:
            user_input = input(f"    [{servo_id:2d}] (Enter/r) | (n) | (q): ").strip().lower()
            if user_input in ("", "r"):
                _do_test(hwi, joint_name, servo_id, init_value, delta_rad)
            elif user_input == "n":
                print()
                break
            elif user_input == "q":
                print("\n[INFO] ")
                _safe_shutdown(hwi)
                return
            else:
                print("     r / n / q")

    print("\n[INFO]  12 ")
    _safe_shutdown(hwi)


def _do_test(hwi, joint_name, servo_id, init_value, delta_rad):
    """This script checks servo direction mapping."""
    target_value = init_value + delta_rad

    # This script checks servo direction mapping.
    print(f"    ->  +{math.degrees(delta_rad):.1f} ...", end="", flush=True)
    hwi.set_position(joint_name, target_value)
    time.sleep(0.6)

    # This script checks servo direction mapping.
    print("  ...", end="", flush=True)
    hwi.set_position(joint_name, init_value)
    time.sleep(0.4)
    print(" OK")


def _safe_shutdown(hwi):
    """This script checks servo direction mapping."""
    print("[INFO]  init_pos ...")
    hwi.set_position_all(hwi.init_pos)
    time.sleep(1)
    print("[INFO] ")
    hwi.turn_off()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO]  (Ctrl+C)")
