#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script records or updates the default standing pose.
This script records or updates the default standing pose.
This script records or updates the default standing pose.
This script records or updates the default standing pose.
This script records or updates the default standing pose.
"""

import json
import os
import sys

# ==========================================
# This script records or updates the default standing pose.
# ==========================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script records or updates the default standing pose.
from runtime.position_hwi import HWI

# This script records or updates the default standing pose.
DEFAULT_POSITION_FILE = "default_position.json"

# This script records or updates the default standing pose.
# This script records or updates the default standing pose.
LEG_GROUPS = {
            "rf": "right_front",
            "lb": "left_back",
        "lf": "left_front",
            "rf": "right_front",
        "lb": "left_back",
    "rb": "right_back"
}


def rad_to_deg(rad):
    """This script records or updates the default standing pose."""
    return rad * 180.0 / 3.14159265359


def get_leg_joints(hwi, leg_prefix):
    """
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    """
    return [
        joint_name
        for joint_name in hwi.joints.keys()
        if joint_name.startswith(leg_prefix)
    ]


def calibrate_one_leg(hwi, leg_key, leg_prefix, result, init_pos_dict):
    """
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    This script records or updates the default standing pose.
    """
    # This script records or updates the default standing pose.
    leg_joint_names = get_leg_joints(hwi, leg_prefix)
    leg_servo_ids = [hwi.joints[joint_name] for joint_name in leg_joint_names]

    print("\n" + "=" * 72)
    print(f": {leg_key.upper()} ({leg_prefix})")
    print("=" * 72)

    # This script records or updates the default standing pose.
    input("...\n")
    hwi.io.disable_torque(leg_servo_ids)
    print(f" {leg_key.upper()}")
    input("/...\n")

    # This script records or updates the default standing pose.
    present_positions = hwi.io.read_present_position(leg_servo_ids)

    # This script records or updates the default standing pose.
    print(f"\n{leg_key.upper()} :")
    print(f"{'joint_name':<32} {'id':<4} {'position(rad)':>14} {'position(deg)':>14}")
    print("-" * 72)

    # This script records or updates the default standing pose.
    for idx, joint_name in enumerate(leg_joint_names):
        joint_id = hwi.joints[joint_name]
        position_rad = float(present_positions[idx])
        position_deg = rad_to_deg(position_rad)

        # This script records or updates the default standing pose.
        result[joint_name] = {
            "id": joint_id,
            "position_rad": round(position_rad, 6),
            "position_deg": round(position_deg, 3),
        }
        # This script records or updates the default standing pose.
        init_pos_dict[joint_name] = round(position_rad, 6)

        # This script records or updates the default standing pose.
        print(
            f"{joint_name:<32} {joint_id:<4} {position_rad:>14.6f} {position_deg:>14.3f}"
        )

    print(f"{leg_key.upper()} ")


def main():
    print("=" * 72)
    print("")
    print("=" * 72)

    print("...")
    hwi = HWI()
    servo_ids = list(hwi.joints.values())
    print("")

    # This script records or updates the default standing pose.
    hwi.turn_on()
    result = {}
    init_pos_dict = {}

    print("\nLB -> RB -> LF -> RF")
    # This script records or updates the default standing pose.
    for leg_key, leg_prefix in LEG_GROUPS.items():
        calibrate_one_leg(hwi, leg_key, leg_prefix, result, init_pos_dict)

    # ==========================================
    # This script records or updates the default standing pose.
    # ==========================================
    print("\n" + "=" * 72)
    print("")
    print(f"{'joint_name':<32} {'id':<4} {'position(rad)':>14} {'position(deg)':>14}")
    print("-" * 72)
    for joint_name, info in result.items():
        print(
            f"{joint_name:<32} {info['id']:<4} "
            f"{info['position_rad']:>14.6f} {info['position_deg']:>14.3f}"
        )

    print("=" * 72)

    # This script records or updates the default standing pose.
    output_path = os.path.join(PROJECT_ROOT, DEFAULT_POSITION_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n{output_path}")

    # ==========================================
    # This script records or updates the default standing pose.
    # ==========================================
    print("\n runtime/position_hwi.py  init_pos:")
    print("init_pos = {")
    for joint_name, value in init_pos_dict.items():
        print(f'    "{joint_name}": {value},')
    print("}")

    # ==========================================
    # This script records or updates the default standing pose.
    # ==========================================
    # This script records or updates the default standing pose.
    # This script records or updates the default standing pose.
    choice = input("\n(y/n y): ").strip().lower()
    if choice != "n":
        hwi.io.set_kps(servo_ids, [2.0] * len(servo_ids))
        print("")
    else:
        print("")

    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # This script records or updates the default standing pose.
        print("\n")
