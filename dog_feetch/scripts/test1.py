#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is a local hardware test entry point.
This script is a local hardware test entry point.
This script is a local hardware test entry point.
This script is a local hardware test entry point.
"""

import argparse
import os
import sys
import time

# ==========================================
# This script is a local hardware test entry point.
# ==========================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script is a local hardware test entry point.
from runtime.position_hwi import HWI


def main():
    # ==========================================
    # This script is a local hardware test entry point.
    # ==========================================
    parser = argparse.ArgumentParser(description="12")
    parser.add_argument(
        "--usb-port",
        default="/dev/ttyUSB0",
        help=" /dev/ttyUSB0",
    )
    # This script is a local hardware test entry point.
    parser.add_argument(
        "--hz",
        type=float,
        default=10.0,
        help="Hz 10",
    )
    args = parser.parse_args()

    # This script is a local hardware test entry point.
    if args.hz <= 0:
        raise ValueError("--hz  0")

    # ==========================================
    # This script is a local hardware test entry point.
    # ==========================================
    hwi = HWI(usb_port=args.usb_port)
    period = 1.0 / args.hz #  ()

    print(f": {args.usb_port}")
    print(f": {args.hz:.2f} Hz")
    print(" Ctrl+C ")

    # ==========================================
    # This script is a local hardware test entry point.
    # ==========================================
    try:
        while True:
            # This script is a local hardware test entry point.
            positions = hwi.get_present_positions()

            # This script is a local hardware test entry point.
            if positions is None:
                print("...")
                time.sleep(period)
                continue

            # This script is a local hardware test entry point.
            # This script is a local hardware test entry point.
            # This script is a local hardware test entry point.
            # This script is a local hardware test entry point.
            print("\033[2J\033[H", end="")

            # This script is a local hardware test entry point.
            print("12 (rad)")
            print("-" * 40)

            # This script is a local hardware test entry point.
            for idx, (joint_name, joint_id) in enumerate(hwi.joints.items()):
                print(
                    f"{idx:02d} | ID {joint_id:02d} | {joint_name:<24} | {positions[idx]:>7.3f}"
                )

            # This script is a local hardware test entry point.
            time.sleep(period)

    except KeyboardInterrupt:
        # This script is a local hardware test entry point.
        print("\n")


if __name__ == "__main__":
    main()
