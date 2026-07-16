#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pickle
import numpy as np
import os
import sys

# ==========================================
# This script runs the learned-policy deployment loop on the real robot.
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script runs the learned-policy deployment loop on the real robot.
from runtime.position_hwi import HWI
from runtime.onnx_infer import OnnxInfer
from runtime.raw_imu import Imu
from runtime.xbox import XBoxController
from runtime.rl_utils import make_action_dict, LowPassActionFilter

HOME_DIR = os.path.expanduser("~")


class RLWalk:
    def __init__(
        self,
        onnx_model_path: str,
        serial_port: str = "/dev/ttyACM0",
        control_freq: float = 50,  # Control loop frequency in Hz.  #  50Hz ( 20ms )
        pid=[30, 0, 0],             # [Kp, Ki, Kd].             #  [Kp, Ki, Kd]
        action_scale=0.25,          # Multiplier applied to policy actions.
        commands=False,             # Enable keyboard/gamepad-style command input.             # /
        pitch_bias=0,               # IMU pitch bias in degrees.               # IMU
        cutoff_frequency=None,
    ):

        self.cmd_max = np.array([0.15, 0.2, 1.0])  # [m/s, m/s, rad/s]
        self.commands = commands

        # This script runs the learned-policy deployment loop on the real robot.
        self.onnx_model_path = onnx_model_path
        self.policy = OnnxInfer(self.onnx_model_path, awd=True)

        self.num_dofs = 12                #  12
        self.max_motor_velocity = 5.24    #  (rad/s)

        self.control_freq = control_freq
        self.pid = pid

        # This script runs the learned-policy deployment loop on the real robot.
        self.action_filter = None
        if cutoff_frequency is not None:
            self.action_filter = LowPassActionFilter(
                self.control_freq, cutoff_frequency
            )

        # This script runs the learned-policy deployment loop on the real robot.
        self.hwi = HWI(serial_port)

        # This script runs the learned-policy deployment loop on the real robot.
        self.start()

        # This script runs the learned-policy deployment loop on the real robot.
        self.imu = Imu(
            sampling_freq=int(self.control_freq)
        )

        self.action_scale = action_scale

        # This script runs the learned-policy deployment loop on the real robot.
        # This script runs the learned-policy deployment loop on the real robot.
        # This script runs the learned-policy deployment loop on the real robot.
        self.last_action = np.zeros(self.num_dofs)
        self.last_last_action = np.zeros(self.num_dofs)
        self.last_last_last_action = np.zeros(self.num_dofs)

        # This script runs the learned-policy deployment loop on the real robot.
        self.init_pos = list(self.hwi.init_pos.values())
        self.joint_signs = list(self.hwi.real_pose_signs_rl.values())

        self.motor_targets = np.array(self.init_pos.copy())

        # This script runs the learned-policy deployment loop on the real robot.
        self.last_commands = [0.0, 0.0, 0.0]

        self.paused = False
        self.command_freq = 20      #  (20Hz)
        if self.commands:
            self.xbox_controller = XBoxController(self.command_freq)

# This script runs the learned-policy deployment loop on the real robot.
# This script runs the learned-policy deployment loop on the real robot.


    def get_obs(self):
        """
        This script runs the learned-policy deployment loop on the real robot.
        This script runs the learned-policy deployment loop on the real robot.
        """
        # This script runs the learned-policy deployment loop on the real robot.
        imu_data = self.imu.get_data()

        # This script runs the learned-policy deployment loop on the real robot.
        dof_pos = self.hwi.get_present_positions()

        # This script runs the learned-policy deployment loop on the real robot.
        dof_vel = self.hwi.get_present_velocities()

        # This script runs the learned-policy deployment loop on the real robot.
        if dof_pos is None or dof_vel is None:
            return None

        if len(dof_pos) != self.num_dofs or len(dof_vel) != self.num_dofs:
            print("ERROR: expected 12 joint positions and velocities")
            return None

        # This script runs the learned-policy deployment loop on the real robot.

        cmds = np.asarray(self.last_commands, dtype=float)[:3] * self.cmd_max
        # This script runs the learned-policy deployment loop on the real robot.
        # This script runs the learned-policy deployment loop on the real robot.
        # This script runs the learned-policy deployment loop on the real robot.
        dof_pos_rel = (dof_pos - self.init_pos) * self.joint_signs
        dof_vel_rl = dof_vel * self.joint_signs

        # This script runs the learned-policy deployment loop on the real robot.
        obs = np.concatenate(
            [
                imu_data["gyro"],              # 3 angular velocity values.              # 3
                imu_data["accelero"],          # 3 acceleration values.          # 3
                cmds,                          # 3 command values.                          # 3
                dof_pos_rel,                   # 12 relative joint positions.                   # 12
                dof_vel_rl * 0.05,             # 12 scaled joint velocities.             # 12 0.05
                self.last_action,              # Previous policy action.              # 12 Action
                self.last_last_action,         # Policy action from two control steps ago.         # 12 Action
                self.last_last_last_action,    # Policy action from three control steps ago.    # 12 Action
            ]
        )
        return obs

    def start(self):
        """This script runs the learned-policy deployment loop on the real robot."""
        n = len(self.hwi.joints)
        kp = float(self.pid[0])
        kd = float(self.pid[2])

        # This script runs the learned-policy deployment loop on the real robot.
        kps = [kp] * n
        kds = [kd] * n
        self.hwi.set_kps(kps)
        self.hwi.set_kds(kds)

        # This script runs the learned-policy deployment loop on the real robot.
        self.hwi.turn_on()
        time.sleep(1.0) #  1

    def run(self):
        """This script runs the learned-policy deployment loop on the real robot."""
        i = 0
        try:
            print("Starting RL Walk loop...")
            start_t = time.time()
            while True:
                t = time.time()

                # This script runs the learned-policy deployment loop on the real robot.
                if self.commands:
                    self.last_commands, self.buttons, _, _ = (
                        self.xbox_controller.get_last_command()
                    )
                    # This script runs the learned-policy deployment loop on the real robot.
                    if self.buttons.A.triggered:
                        self.paused = not self.paused
                        if self.paused:
                            print("=== PAUSE ===")
                        else:
                            print("=== UNPAUSE ===")

                # This script runs the learned-policy deployment loop on the real robot.
                if self.paused:
                    time.sleep(0.1)
                    continue

                # This script runs the learned-policy deployment loop on the real robot.
                obs = self.get_obs()
                if obs is None:
                    continue

                # This script runs the learned-policy deployment loop on the real robot.
                action = np.asarray(self.policy.infer(obs), dtype=float)
                print(action)

                # This script runs the learned-policy deployment loop on the real robot.
                self.last_last_last_action = self.last_last_action.copy()
                self.last_last_action = self.last_action.copy()
                self.last_action = action.copy()

                # This script runs the learned-policy deployment loop on the real robot.
                # This script runs the learned-policy deployment loop on the real robot.
                self.motor_targets = (
                    self.init_pos + action * self.action_scale * self.joint_signs
                )

                # This script runs the learned-policy deployment loop on the real robot.
                if self.action_filter is not None:
                    self.action_filter.push(self.motor_targets)
                    filtered_motor_targets = self.action_filter.get_filtered_action()
                    # This script runs the learned-policy deployment loop on the real robot.
                    if (time.time() - start_t > 1):
                        self.motor_targets = filtered_motor_targets

                # This script runs the learned-policy deployment loop on the real robot.
                action_dict = make_action_dict(
                    self.motor_targets, list(self.hwi.joints.keys())
                )
                print(action_dict)
                # This script runs the learned-policy deployment loop on the real robot.
                self.hwi.set_position_all(action_dict)
                i += 1

                # ==========================================
                # This script runs the learned-policy deployment loop on the real robot.
                # ==========================================
                took = time.time() - t # +

                # This script runs the learned-policy deployment loop on the real robot.
                # This script runs the learned-policy deployment loop on the real robot.
                if (1 / self.control_freq - took) < 0:
                    print(
                        "Policy control budget exceeded by",
                        np.around(took - 1 / self.control_freq, 3), "seconds!"
                    )
                # This script runs the learned-policy deployment loop on the real robot.
                time.sleep(max(0, 1 / self.control_freq - took))

        except KeyboardInterrupt:
            # This script runs the learned-policy deployment loop on the real robot.
            pass
        finally:
            # ==========================================
            # This script runs the learned-policy deployment loop on the real robot.
            # ==========================================
            print("\nTURNING OFF AND CLEANING UP...")
            try:
                if self.commands and hasattr(self, "xbox_controller"):
                    self.xbox_controller.close()
            except Exception as e:
                print("Failed to close controller:", e)

            try:
                self.hwi.turn_off() #  12
                print("[SUCCESS] ")
            except Exception as e:
                print("Failed to turn off motors:", e)


if __name__ == "__main__":
    import argparse

    # This script runs the learned-policy deployment loop on the real robot.
    parser = argparse.ArgumentParser(description="Run the RL walking controller on the real robot.")
    parser.add_argument("--onnx_model_path", type=str, default="/home/elf/Desktop/Learn-It-All-deployment-sim2real-main/2026_06_13_125153_32112640.onnx")
    parser.add_argument("-a", "--action_scale", type=float, default=0.25)
    parser.add_argument("-p", type=int, default=30, help=" Kp")
    parser.add_argument("-i", type=int, default=0)
    parser.add_argument("-d", type=int, default=0, help=" Kd")
    parser.add_argument("-c", "--control_freq", type=int, default=50)
    parser.add_argument("--pitch_bias", type=float, default=0, help="IMU pitch bias in degrees")
    parser.add_argument(
        "--commands",
        action="store_true",
        default=True,
        help="",
    )
    # This script runs the learned-policy deployment loop on the real robot.
    parser.add_argument("--cutoff_frequency", type=float, default=None)

    args = parser.parse_args()
    pid = [args.p, args.i, args.d]

    print("Done parsing args")
    # This script runs the learned-policy deployment loop on the real robot.
    rl_walk = RLWalk(
        args.onnx_model_path,
        action_scale=args.action_scale,
        pid=pid,
        control_freq=args.control_freq,
        commands=args.commands,
        pitch_bias=args.pitch_bias,
        cutoff_frequency=args.cutoff_frequency,
    )
    print("Done instantiating RLWalk")

    # This script runs the learned-policy deployment loop on the real robot.
    rl_walk.run()
