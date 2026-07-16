#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import pickle
from queue import Queue
from threading import Thread
import time
import platform

# This module reads raw WitMotion IMU data through the vendor protocol library.
import lib.device_model as deviceModel
from lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
from lib.protocol_resolver.roles.wit_protocol_resolver import WitProtocolResolver

# This module reads raw WitMotion IMU data through the vendor protocol library.
GRAVITY = 9.81           # g  m/s
DEG2RAD = np.pi / 180    # deg/s  rad/s MuJoCo

class Imu:
    def __init__(
        self, sampling_freq
    ):
        """
        This module reads raw WitMotion IMU data through the vendor protocol library.
        This module reads raw WitMotion IMU data through the vendor protocol library.
          - accelero: m/s
          - gyro: rad/s
        """
        self.sampling_freq = sampling_freq

        # ==========================================
        # This module reads raw WitMotion IMU data through the vendor protocol library.
        # ==========================================
        self._device = deviceModel.DeviceModel(
            "JY901",
            WitProtocolResolver(),
            JY901SDataProcessor(),
            "51_0"
        )
        if platform.system().lower() == 'linux':
            self._device.serialConfig.portName = "/dev/ttyUSB0"
        else:
            self._device.serialConfig.portName = "COM17"
        self._device.serialConfig.baud = 921600
        self._device.openDevice()

        # This module reads raw WitMotion IMU data through the vendor protocol library.
        self.last_imu_data = {
            "gyro": [0, 0, 0],
            "accelero": [0, 0, 0],
        }

        # This module reads raw WitMotion IMU data through the vendor protocol library.
        self.imu_queue = Queue(maxsize=1)

        # This module reads raw WitMotion IMU data through the vendor protocol library.
        Thread(target=self.imu_worker, daemon=True).start()

    def imu_worker(self):
        """This module reads raw WitMotion IMU data through the vendor protocol library."""
        while True:
            s = time.time()
            try:
                # This module reads raw WitMotion IMU data through the vendor protocol library.
                gyro = (np.array([
                    self._device.getDeviceData("gyroX"),
                    self._device.getDeviceData("gyroY"),
                    self._device.getDeviceData("gyroZ")
                ]) * DEG2RAD).copy()

                # This module reads raw WitMotion IMU data through the vendor protocol library.
                accelero = (np.array([
                    self._device.getDeviceData("accX"),
                    self._device.getDeviceData("accY"),
                    self._device.getDeviceData("accZ")
                ]) * GRAVITY).copy()
            except Exception as e:
                print("[IMU]:", e)
                continue

            # This module reads raw WitMotion IMU data through the vendor protocol library.
            if gyro is None or accelero is None:
                continue

            # This module reads raw WitMotion IMU data through the vendor protocol library.
            if gyro.any() is None or accelero.any() is None:
                continue

            # This module reads raw WitMotion IMU data through the vendor protocol library.
            data = {
                "gyro": gyro,
                "accelero": accelero,
            }

            # This module reads raw WitMotion IMU data through the vendor protocol library.
            self.imu_queue.put(data)

            # This module reads raw WitMotion IMU data through the vendor protocol library.
            took = time.time() - s
            time.sleep(max(0, 1 / self.sampling_freq - took))

    def get_data(self):
        """
        This module reads raw WitMotion IMU data through the vendor protocol library.
        This module reads raw WitMotion IMU data through the vendor protocol library.
        """
        try:
            self.last_imu_data = self.imu_queue.get(False)  # False
        except Exception:
            pass

        return self.last_imu_data


if __name__ == "__main__":
    # This module reads raw WitMotion IMU data through the vendor protocol library.
    imu = Imu(50)
    while True:
        data = imu.get_data()

        # This module reads raw WitMotion IMU data through the vendor protocol library.
        print("gyro (rad/s)", np.around(data["gyro"], 5))
        print("accelero (m/s)", np.around(data["accelero"], 4))
        print("---")

        # This module reads raw WitMotion IMU data through the vendor protocol library.
        time.sleep(1 / 25)


