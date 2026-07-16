#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time
from typing import Dict, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from runtime.position_hwi import HWI


def probe_id(hwi: HWI, servo_id: int):
    """Return (ok, position_or_err)."""
    try:
        pos = hwi.io.read_present_position([servo_id])[0]
        return True, float(pos)
    except Exception as e:
        return False, str(e)


def scan_online_ids(hwi: HWI, scan_min: int, scan_max: int) -> List[int]:
    online = []
    for servo_id in range(scan_min, scan_max + 1):
        ok, _ = probe_id(hwi, servo_id)
        if ok:
            online.append(servo_id)
    return online


def nudge_joint(hwi: HWI, joint_name: str, servo_id: int, delta: float, hold: float):
    ok, val = probe_id(hwi, servo_id)
    if not ok:
        print(f"ID {servo_id:02d} ({joint_name}) ")
        return

    current = float(val)
    try:
        hwi.set_kp(servo_id, 6.0)
    except Exception as e:
        print(f" Kp : {e}")

    try:
        hwi.io.write_goal_position([servo_id], [current + delta])
        time.sleep(hold)
        hwi.io.write_goal_position([servo_id], [current])
        time.sleep(hold)
        hwi.io.write_goal_position([servo_id], [current - delta])
        time.sleep(hold)
        hwi.io.write_goal_position([servo_id], [current])
        time.sleep(hold)
        print(
            f" {joint_name} (ID {servo_id:02d}) {current:+.3f} rad {delta:.3f} rad"
        )
    except Exception as e:
        print(f" {joint_name} (ID {servo_id:02d}): {e}")


def main():
    parser = argparse.ArgumentParser(
        description=" ID "
    )
    parser.add_argument(
        "--usb-port",
        default="/dev/ttyUSB0",
        help=" /dev/ttyUSB0",
    )
    parser.add_argument("--scan-min", type=int, default=0, help=" ID")
    parser.add_argument("--scan-max", type=int, default=20, help=" ID")
    parser.add_argument(
        "--delta",
        type=float,
        default=0.20,
        help="rad 0.20",
    )
    parser.add_argument(
        "--hold",
        type=float,
        default=0.35,
        help=" 0.35",
    )
    args = parser.parse_args()

    if args.scan_min < 0 or args.scan_max < args.scan_min:
        raise ValueError(" 0 <= scan-min <= scan-max")

    hwi = HWI(usb_port=args.usb_port)
    configured: Dict[str, int] = hwi.joints

    print(f": {args.usb_port}")
    print("\n[1]  -> ID")
    print("-" * 72)
    for idx, (joint_name, servo_id) in enumerate(configured.items()):
        print(f"{idx:02d} | ID {servo_id:02d} | {joint_name}")

    print("\n[2]  ID ")
    print("-" * 72)
    configured_ids = set(configured.values())
    ok_count = 0
    fail_count = 0
    for idx, (joint_name, servo_id) in enumerate(configured.items()):
        ok, val = probe_id(hwi, servo_id)
        if ok:
            ok_count += 1
            print(
                f"{idx:02d} | ID {servo_id:02d} | {joint_name:<24} | ONLINE | pos={val:+.3f} rad"
            )
        else:
            fail_count += 1
            print(
                f"{idx:02d} | ID {servo_id:02d} | {joint_name:<24} | MISSING | {val}"
            )

    print("\n[3]  ID")
    print("-" * 72)
    online_ids = scan_online_ids(hwi, args.scan_min, args.scan_max)
    unknown_ids = [sid for sid in online_ids if sid not in configured_ids]

    print(f": [{args.scan_min}, {args.scan_max}]")
    print(f" ID: {online_ids if online_ids else ''}")
    print(f" ID: {unknown_ids if unknown_ids else ''}")

    print("\n")
    print("-" * 72)
    print(f": {len(configured)}")
    print(f": {ok_count}")
    print(f": {fail_count}")
    if fail_count == 0 and len(unknown_ids) == 0:
        print("ID ")
    else:
        print(" ID")

    print("\n[4] ")
    print("-" * 72)
    print("")
    print("1) ")
    print("2)  s ")
    print("3)  q ")

    for idx, (joint_name, servo_id) in enumerate(configured.items()):
        cmd = input(
            f"\n[{idx+1:02d}/{len(configured)}] {joint_name} (ID {servo_id:02d}) "
            ": "
        ).strip().lower()
        if cmd == "q":
            print("")
            break
        if cmd == "s":
            print("")
            continue
        nudge_joint(hwi, joint_name, servo_id, delta=args.delta, hold=args.hold)


if __name__ == "__main__":
    main()
