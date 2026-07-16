#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script moves configured servos toward their center positions.
This script moves configured servos toward their center positions.
"""

import argparse
import os
import sys
import time

# ==========================================
# This script moves configured servos toward their center positions.
# ==========================================
# This script moves configured servos toward their center positions.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This script moves configured servos toward their center positions.
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script moves configured servos toward their center positions.
from runtime.position_hwi import HWI


def main():
    # ==========================================
    # This script moves configured servos toward their center positions.
    # ==========================================
    parser = argparse.ArgumentParser(description="12")

    # This script moves configured servos toward their center positions.
    parser.add_argument(
        "--usb-port",
        default="/dev/ttyUSB0",
        help=" /dev/ttyUSB0",
    )
    # This script moves configured servos toward their center positions.
    parser.add_argument(
        "--kp",
        type=float,
        default=8.0,
        help=" 8.0",
    )
    # This script moves configured servos toward their center positions.
    parser.add_argument(
        "--hold-seconds",
        type=float,
        default=2.0,
        help="",
    )
    args = parser.parse_args()

    # ==========================================
    # This script moves configured servos toward their center positions.
    # ==========================================
    print(f": {args.usb_port}")
    # This script moves configured servos toward their center positions.
    hwi = HWI(usb_port=args.usb_port)

    # This script moves configured servos toward their center positions.
    servo_ids = list(hwi.joints.values())

    # ==========================================
    # This script moves configured servos toward their center positions.
    # ==========================================
    # This script moves configured servos toward their center positions.
    print(f" kp={args.kp}")
    hwi.io.set_kps(servo_ids, [float(args.kp)] * len(servo_ids))

    # This script moves configured servos toward their center positions.
    print("12  -> 0 rad")
    hwi.set_position_all(hwi.zero_pos)

    # This script moves configured servos toward their center positions.
    print(f" {args.hold_seconds:.1f}s ...")
    time.sleep(max(args.hold_seconds, 0.0))
    print("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # This script moves configured servos toward their center positions.
        print("\n")
