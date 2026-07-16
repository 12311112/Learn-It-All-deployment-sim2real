#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script provides a GUI for joint calibration.
"""

import argparse
import math
import os
import sys       # Python
import time
from typing import Dict

# This script provides a GUI for joint calibration.
# This script provides a GUI for joint calibration.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This script provides a GUI for joint calibration.
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script provides a GUI for joint calibration.
# This script provides a GUI for joint calibration.
# This script provides a GUI for joint calibration.
LEG_JOINTS = {
    "left_front": ["left_front_hip_joint", "left_front_knee_joint", "left_front_ankle_joint"],
    "right_front": ["right_front_hip_joint", "right_front_knee_joint", "right_front_ankle_joint"],
    "left_back": ["left_back_hip_joint", "left_back_knee_joint", "left_back_ankle_joint"],
    "right_back": ["right_back_hip_joint", "right_back_knee_joint", "right_back_ankle_joint"],
}


def mech_to_servo(hwi, joint_name: str, mech_angle: float) -> float:
    """
    This script provides a GUI for joint calibration.

    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.

    This script provides a GUI for joint calibration.
    """
    # This script provides a GUI for joint calibration.
    real_local = hwi.real_pose[joint_name]

    # This script provides a GUI for joint calibration.
    # This script provides a GUI for joint calibration.
    # This script provides a GUI for joint calibration.
    return (mech_angle - real_local) * hwi.real_pose_signs.get(joint_name, 1.0) + hwi.init_pos[joint_name]


def send_mech_pose(hwi, mech_pose: Dict[str, float]):
    """
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    """
    ids = []      # ID 123
    positions = []

    # This script provides a GUI for joint calibration.
    for joint_name, mech in mech_pose.items():
        ids.append(hwi.joints[joint_name])                    # ID
        positions.append(mech_to_servo(hwi, joint_name, mech))

    # This script provides a GUI for joint calibration.
    hwi.io.write_goal_position(ids, positions)


def setup_gui():
    """
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    This script provides a GUI for joint calibration.
    """
    import pybullet as p #  PyBullet

    # This script provides a GUI for joint calibration.
    if p.getConnectionInfo()["isConnected"] == 0:
        p.connect(p.GUI)

    # This script provides a GUI for joint calibration.
    sliders = {
        # This script provides a GUI for joint calibration.
        "delta": p.addUserDebugParameter("target delta(rad)", -1.2, 1.2, 0.0),
        # This script provides a GUI for joint calibration.
        "period": p.addUserDebugParameter("sweep period(s)", 0.4, 4.0, 1.2),
        # This script provides a GUI for joint calibration.
        "mode": p.addUserDebugParameter("mode: 0=hold 1=sine", 0, 1, 0),
    }
    return p, sliders


def main():
    """This script provides a GUI for joint calibration."""

    # This script provides a GUI for joint calibration.
    # This script provides a GUI for joint calibration.
    parser = argparse.ArgumentParser(description=" GUI")
    parser.add_argument("--usb-port", default="/dev/tty/ACM0")  # USBLinux
    parser.add_argument("--dt", type=float, default=0.02)      # 0.02150
    parser.add_argument("--duration", type=float, default=0.0, help="0=")
    parser.add_argument(
        "--leg",
        required=True,
        choices=["left_front", "right_front", "left_back", "right_back"],
        help="",
    )
    parser.add_argument(
        "--joint",
        required=True,
        choices=["hip", "knee", "ankle", "all"], #  all
        help="",
    )
    args = parser.parse_args()

    # This script provides a GUI for joint calibration.
    from runtime.position_hwi import HWI

    # This script provides a GUI for joint calibration.
    if args.joint == "all":
        active_joints = LEG_JOINTS[args.leg]          #  all3
    else:
        # This script provides a GUI for joint calibration.
        joint_idx = {"hip": 0, "knee": 1, "ankle": 2}[args.joint]
        active_joints = [LEG_JOINTS[args.leg][joint_idx]]

    # This script provides a GUI for joint calibration.
    hwi = HWI(usb_port=args.usb_port)
    print(f"[INFO] connect: {args.usb_port}")
    print(f"[INFO] active_leg={args.leg}, active_joints={active_joints}")
    print("[INFO] angle map: servo = (mech - real_pose) * real_pose_sign + init_pos + offset")

    # This script provides a GUI for joint calibration.
    for joint_name in active_joints:
        print(f"[INFO] real_pose_sign[{joint_name}]={int(hwi.real_pose_signs.get(joint_name, 1.0)):+d}")

    # This script provides a GUI for joint calibration.
    hwi.turn_on()

    # This script provides a GUI for joint calibration.
    p, sliders = setup_gui()
    print("[INFO] GUI ready, press q or ESC to quit")

    # This script provides a GUI for joint calibration.
    base_pose = hwi.real_pose.copy()
    start_t = time.time()
    next_t = start_t
    tick = 0

    # This script provides a GUI for joint calibration.
    try:
        while True:
            now = time.time()
            # This script provides a GUI for joint calibration.
            if args.duration > 0.0 and now - start_t >= args.duration:
                break

            # This script provides a GUI for joint calibration.
            keys = p.getKeyboardEvents()
            if keys.get(ord("q")) or keys.get(27):
                break

            # This script provides a GUI for joint calibration.
            # This script provides a GUI for joint calibration.
            delta = float(p.readUserDebugParameter(sliders["delta"]))
            period = max(0.4, float(p.readUserDebugParameter(sliders["period"])))  # 0.4
            mode = int(round(p.readUserDebugParameter(sliders["mode"])))

            # This script provides a GUI for joint calibration.
            mech_pose = base_pose.copy()

            # This script provides a GUI for joint calibration.
            if mode == 0:
                # This script provides a GUI for joint calibration.
                delta_now = delta
            else:
                # This script provides a GUI for joint calibration.
                # This script provides a GUI for joint calibration.
                # This script provides a GUI for joint calibration.
                phase = (now - start_t) * (2.0 * math.pi / period)
                delta_now = delta * math.sin(phase)

            # This script provides a GUI for joint calibration.
            for joint_name in active_joints:
                mech_pose[joint_name] = base_pose[joint_name] + delta_now

            # This script provides a GUI for joint calibration.
            send_mech_pose(hwi, mech_pose)

            # This script provides a GUI for joint calibration.
            if tick % 50 == 0:
                for joint_name in active_joints:
                    target = mech_pose[joint_name]
                    sign = hwi.real_pose_signs.get(joint_name, 1.0)
                    servo = mech_to_servo(hwi, joint_name, target)
                    # This script provides a GUI for joint calibration.
                    print(
                        f"[DEBUG] {joint_name} mech={target:+.4f} "
                        f"real={hwi.real_pose[joint_name]:+.4f} sign={int(sign):+d} init={hwi.init_pos[joint_name]:+.4f} "
                        f"servo={servo:+.4f} mode={'hold' if mode == 0 else 'sine'}"
                    )
            tick += 1 #  1

            # This script provides a GUI for joint calibration.
            next_t += args.dt
            sleep_t = next_t - time.time()
            if sleep_t > 0:
                time.sleep(sleep_t)
            else:
                next_t = time.time()

    except KeyboardInterrupt:
        # This script provides a GUI for joint calibration.
        pass

    finally:
        # This script provides a GUI for joint calibration.
        # This script provides a GUI for joint calibration.
        print("[INFO] stopping...")

        # This script provides a GUI for joint calibration.
        try:
            hwi.set_position_all(hwi.init_pos)
            time.sleep(0.5)
        except Exception:
            pass

        # This script provides a GUI for joint calibration.
        try:
            p.disconnect()
        except Exception:
            pass

        # This script provides a GUI for joint calibration.
        # This script provides a GUI for joint calibration.
        hwi.turn_off()
        print("[INFO] torque disabled")


if __name__ == "__main__":
    main()
