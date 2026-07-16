#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import rustypot  #  (Feetech)  ( Rust  Python )

class HWI:
    def __init__(self, usb_port: str = "/dev/ttyACM0"):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """

        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        self.joints = {
            "right_front_hip_joint": 6,
            "right_front_knee_joint": 7,
            "right_front_ankle_joint": 8,

            "left_front_hip_joint": 0,
            "left_front_knee_joint": 4,   # ID 4
            "left_front_ankle_joint": 5,  # ID 5

            "right_back_hip_joint": 9,    # ID 9
            "right_back_knee_joint": 10,  # ID 10
            "right_back_ankle_joint": 11, # ID 11

            "left_back_hip_joint": 3,
            "left_back_knee_joint": 1,    # ID 1
            "left_back_ankle_joint": 2,   # ID 2
        }

        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        self.init_pos = {
        # "right_front_hip_joint": -0.090,
        # "right_front_knee_joint": 0.0292000,
        # "right_front_ankle_joint": -0.3315300,
        # "left_front_hip_joint": 0.07,
        # "left_front_knee_joint": 0.182000,
        # "left_front_ankle_joint": 0.015000,
        # "right_back_hip_joint": -0.140000,
        # "right_back_knee_joint": 0.583000,
        # "right_back_ankle_joint": 0.003000,

        # "left_back_hip_joint": -0.053000,
        # "left_back_knee_joint": -0.605000,
        # "left_back_ankle_joint": 0.0184000,


    "right_front_hip_joint": 0.003068,
    "right_front_knee_joint": -0.136524,
    "right_front_ankle_joint": 0.291456,
    "left_front_hip_joint": -0.058291,
    "left_front_knee_joint": 0.312932,
    "left_front_ankle_joint": -0.408039,
    "right_back_hip_joint": -0.218117,
    "right_back_knee_joint": 0.042951,
    "right_back_ankle_joint": 0.430097,
    "left_back_hip_joint": 0.0109825,
    "left_back_knee_joint": -0.133456,
    "left_back_ankle_joint": -0.268738,
        }

        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        self.real_pose_signs_rl = {
            "right_front_hip_joint": 1.0,
            "right_front_knee_joint": 1.0,
            "right_front_ankle_joint": 1.0,

            "left_front_hip_joint": 1.0,
            "left_front_knee_joint": -1.0,
            "left_front_ankle_joint": -1.0,

            "right_back_hip_joint": -1.0,
            "right_back_knee_joint": 1.0,
            "right_back_ankle_joint": 1.0,

            "left_back_hip_joint": -1.0,
            "left_back_knee_joint": -1.0,
            "left_back_ankle_joint": -1.0,
        }




        ##for ik
        self.real_pose = {  #####################
        "left_front_hip_joint":0 , ##+++++++
        "left_front_knee_joint":-0.96754,#-----
        "left_front_ankle_joint":1.850729,###-----

        "left_back_hip_joint": 0,#------
        "left_back_knee_joint": -0.96754,#----
        "left_back_ankle_joint": 1.850729,#-----

        "right_front_hip_joint": 0,#+++
        "right_front_knee_joint": -0.96754,#++++
        "right_front_ankle_joint": 1.850729,#+++++

        "right_back_hip_joint":  0,#----
        "right_back_knee_joint": -0.96754,####+++++
        "right_back_ankle_joint": 1.850729,#+++++
        }


        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        self.real_pose_signs = {  #####################

        "right_front_hip_joint": -1.0,
        "right_front_knee_joint": 1.0,
        "right_front_ankle_joint": -1.0,

        "left_front_hip_joint": 1.0,
        "left_front_knee_joint": 1.0,
        "left_front_ankle_joint": 1.0,

        "left_back_hip_joint": -1.0,
        "left_back_knee_joint": 1.0,
        "left_back_ankle_joint": 1.0,


        "right_back_hip_joint": 1.0,
        "right_back_knee_joint": 1.0,
        "right_back_ankle_joint": -1.0,
    }



        # This module maps robot joints to Feetech servo commands and feedback.
        # This module maps robot joints to Feetech servo commands and feedback.
        self.joints_offsets = {joint: 0.0 for joint in self.joints.keys()}

        # This module maps robot joints to Feetech servo commands and feedback.
        self.kps = np.ones(len(self.joints)) * 30            #  ( Stiffness)
        self.kds = np.ones(len(self.joints)) * 0             #  ( Damping)
        self.low_torque_kps = np.ones(len(self.joints)) * 2

        # This module maps robot joints to Feetech servo commands and feedback.
        self.io = rustypot.feetech(usb_port, 1000000)
        self.real_pose_signs = {}

    def set_kps(self, kps):
        """This module maps robot joints to Feetech servo commands and feedback."""
        self.kps = kps
        self.io.set_kps(list(self.joints.values()), self.kps)

    def set_kds(self, kds):
        """This module maps robot joints to Feetech servo commands and feedback."""
        self.kds = kds
        self.io.set_kds(list(self.joints.values()), self.kds)

    def set_kp(self, id, kp):
        """This module maps robot joints to Feetech servo commands and feedback."""
        self.io.set_kps([id], [kp])

    def turn_on(self):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """
        # This module maps robot joints to Feetech servo commands and feedback.
        self.io.set_kps(list(self.joints.values()), self.low_torque_kps)
        print("turn on : low KPS set")
        time.sleep(1)

        # This module maps robot joints to Feetech servo commands and feedback.
        self.set_position_all(self.init_pos)
        print("turn on : init pos set")
        time.sleep(1)

        # This module maps robot joints to Feetech servo commands and feedback.
        self.io.set_kps(list(self.joints.values()), self.kps)
        print("turn on : high kps")

    def turn_off(self):
        """This module maps robot joints to Feetech servo commands and feedback."""
        self.io.disable_torque(list(self.joints.values()))

    def set_position(self, joint_name, pos):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """
        id = self.joints[joint_name]
        # This module maps robot joints to Feetech servo commands and feedback.
        pos = pos + self.joints_offsets[joint_name]
        self.io.write_goal_position([id], [pos])

    def set_position_all(self, joints_positions):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """
        ids = []
        positions = []

        # This module maps robot joints to Feetech servo commands and feedback.
        for joint, position in joints_positions.items():
            if joint not in self.joints:
                raise KeyError(f"Unknown joint name: {joint}")
            ids.append(self.joints[joint])
            # This module maps robot joints to Feetech servo commands and feedback.
            positions.append(position + self.joints_offsets[joint])

        # This module maps robot joints to Feetech servo commands and feedback.
        self.io.write_goal_position(ids, positions)

    def get_present_positions(self, ignore=[]):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """
        try:
            # This module maps robot joints to Feetech servo commands and feedback.
            present_positions = self.io.read_present_position(
                list(self.joints.values())
            )
        except Exception as e:
            print(f": {e}")
            return None

        # This module maps robot joints to Feetech servo commands and feedback.
        present_positions = [
            pos - self.joints_offsets[joint]
            for joint, pos in zip(self.joints.keys(), present_positions)
            if joint not in ignore
        ]
        return np.array(np.around(present_positions, 3))

    def get_present_velocities(self, rad_s=True, ignore=[]):
        """
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        This module maps robot joints to Feetech servo commands and feedback.
        """
        try:
            # This module maps robot joints to Feetech servo commands and feedback.
            present_velocities = self.io.read_present_velocity(
                list(self.joints.values())
            )
        except Exception as e:
            print(f": {e}")
            return None

        # This module maps robot joints to Feetech servo commands and feedback.
        present_velocities = [
            vel
            for joint, vel in zip(self.joints.keys(), present_velocities)
            if joint not in ignore
        ]
        return np.array(np.around(present_velocities, 3))
