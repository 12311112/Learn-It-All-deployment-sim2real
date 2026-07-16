#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script inspects servo feedback and motor behavior.
This script inspects servo feedback and motor behavior.
"""
import os
import sys
import time
import numpy as np
import traceback

# ==========================================
# This script inspects servo feedback and motor behavior.
# ==========================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# This script inspects servo feedback and motor behavior.
from runtime.position_hwi import HWI


def main():
    print("Initializing hardware interface...")
    try:
        print("Attempting to connect to motor controller...")
        # This script inspects servo feedback and motor behavior.
        hwi = HWI()
        print("Successfully connected to hardware!")
    except Exception as e:
        # This script inspects servo feedback and motor behavior.
        print(f"Error connecting to hardware: {e}")
        print(f"Error details: {traceback.format_exc()}")
        print("Check that the robot is powered on and USB connection is correct.")
        return

    # ==========================================
    # This script inspects servo feedback and motor behavior.
    # ==========================================
    print("\nTurning on motors with low torque (one by one)...")
    unresponsive_motors = []

    for joint_name, joint_id in hwi.joints.items():
        try:
            print(f"Setting low torque for motor '{joint_name}' (ID: {joint_id})...")
            # This script inspects servo feedback and motor behavior.
            hwi.io.set_kps([joint_id], [hwi.low_torque_kps[0]])
            print(f" Low torque set successfully for motor '{joint_name}' (ID: {joint_id}).")
        except Exception as e:
            # This script inspects servo feedback and motor behavior.
            print(f" Error setting low torque for motor '{joint_name}' (ID: {joint_id}): {e}")
            print(f"Error details: {traceback.format_exc()}")
            unresponsive_motors.append((joint_name, joint_id))

    # ==========================================
    # This script inspects servo feedback and motor behavior.
    # ==========================================
    print("\nChecking if all motors are responsive...")

    for joint_name, joint_id in hwi.joints.items():
        # This script inspects servo feedback and motor behavior.
        if (joint_name, joint_id) in unresponsive_motors:
            print(f"Skipping previously unresponsive motor: '{joint_name}' (ID: {joint_id})")
            continue

        print(f"Attempting to read position from motor '{joint_name}' (ID: {joint_id})...")
        try:
            # This script inspects servo feedback and motor behavior.
            position = hwi.io.read_present_position([joint_id])
            print(f" Motor '{joint_name}' (ID: {joint_id}) is responsive. Position: {position[0]:.3f}")
        except Exception as e:
            print(f" Error accessing motor '{joint_name}' (ID: {joint_id}): {e}")
            print(f"Error details for motor {joint_id}: {traceback.format_exc()}")
            unresponsive_motors.append((joint_name, joint_id))

    # ==========================================
    # This script inspects servo feedback and motor behavior.
    # ==========================================
    if unresponsive_motors:
        print("\nWARNING: Some motors are not responsive!")
        print("Unresponsive motors:", unresponsive_motors)
        # This script inspects servo feedback and motor behavior.
        continue_anyway = input("Do you want to continue anyway  (y/n): ").lower()
        if continue_anyway != 'y':
            print("Exiting...")
            try:
                # This script inspects servo feedback and motor behavior.
                print("Attempting to turn off responsive motors before exiting...")
                for joint_name, joint_id in hwi.joints.items():
                    if (joint_name, joint_id) not in unresponsive_motors:
                        try:
                            hwi.io.disable_torque([joint_id])
                            print(f"Disabled torque for motor '{joint_name}' (ID: {joint_id})")
                        except:
                            pass
            except:
                pass
            return

    # ==========================================
    # This script inspects servo feedback and motor behavior.
    # ==========================================
    print("\n--- Motor Movement Test ---")
    print("This will move each motor by a small amount to check if it's working correctly.")
    input("Press Enter to begin the movement test...")

    for joint_name, joint_id in hwi.joints.items():
        # This script inspects servo feedback and motor behavior.
        if (joint_name, joint_id) in unresponsive_motors:
            print(f"Skipping unresponsive motor: '{joint_name}' (ID: {joint_id})")
            continue

        print(f"\nTesting motor: '{joint_name}' (ID: {joint_id})")
        test_this_motor = input(f"Test this motor  (Enter/y for yes, n to skip, q to quit): ").lower()

        if test_this_motor == 'q':
            print("Exiting movement test...")
            break

        if test_this_motor == 'n':
            print(f"Skipping '{joint_name}' (ID: {joint_id})")
            continue

        try:
            # This script inspects servo feedback and motor behavior.
            print(f"Reading current position from motor '{joint_name}' (ID: {joint_id})...")
            current_position = hwi.io.read_present_position([joint_id])[0]
            print(f"Current position: {current_position:.3f}")

            # This script inspects servo feedback and motor behavior.
            # This script inspects servo feedback and motor behavior.
            # This script inspects servo feedback and motor behavior.
            # This script inspects servo feedback and motor behavior.
            test_position = current_position + 1.1

            # This script inspects servo feedback and motor behavior.
            print(f"Moving motor '{joint_name}' (ID: {joint_id}) to test position: {test_position:.3f}...")
            hwi.io.write_goal_position([joint_id], [test_position])
            time.sleep(1)

            # This script inspects servo feedback and motor behavior.
            print(f"Reading new position from motor '{joint_name}' (ID: {joint_id})...")
            new_position = hwi.io.read_present_position([joint_id])[0]
            print(f"New position: {new_position:.3f}")

            # This script inspects servo feedback and motor behavior.
            print(f"Returning motor '{joint_name}' (ID: {joint_id}) to original position...")
            hwi.io.write_goal_position([joint_id], [current_position])
            time.sleep(1)

            print(f" Motor '{joint_name}' (ID: {joint_id}) movement test completed.")

        except Exception as e:
            print(f"Error testing motor '{joint_name}' (ID: {joint_id}): {e}")
            print(f"Error details: {traceback.format_exc()}")

    # ==========================================
    # This script inspects servo feedback and motor behavior.
    # ==========================================
    print("\nTurning off motors one by one...")
    for joint_name, joint_id in hwi.joints.items():
        if (joint_name, joint_id) in unresponsive_motors:
            print(f"Skipping turning off unresponsive motor: '{joint_name}' (ID: {joint_id})")
            continue

        try:
            print(f"Disabling torque for motor '{joint_name}' (ID: {joint_id})...")
            # This script inspects servo feedback and motor behavior.
            hwi.io.disable_torque([joint_id])
            print(f" Motor '{joint_name}' (ID: {joint_id}) turned off successfully.")
        except Exception as e:
            print(f" Error turning off motor '{joint_name}' (ID: {joint_id}): {e}")
            print(f"Error details: {traceback.format_exc()}")

    print("\nMotor test completed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # ==========================================
        # This script inspects servo feedback and motor behavior.
        # ==========================================
        # This script inspects servo feedback and motor behavior.
        print("\nScript interrupted by user. Attempting to turn off motors...")
        try:
            print("Initializing HWI to turn off motors...")
            hwi = HWI()
            # This script inspects servo feedback and motor behavior.
            for joint_name, joint_id in hwi.joints.items():
                try:
                    print(f"Turning off motor '{joint_name}' (ID: {joint_id})...")
                    hwi.io.disable_torque([joint_id])
                    print(f" Motor '{joint_name}' (ID: {joint_id}) turned off successfully.")
                except Exception as e:
                    print(f" Error turning off motor '{joint_name}' (ID: {joint_id}): {e}")
        except Exception as e:
            print(f"Error initializing HWI to turn off motors: {e}")
            print(f"Error details: {traceback.format_exc()}")
