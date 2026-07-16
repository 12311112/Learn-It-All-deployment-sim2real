# Learn-It-All Deployment Sim2Real

This repository contains the real-robot deployment part of the Learn-It-All quadruped robot project. It focuses on running learned ONNX control policies and educational model-based controllers on the physical Feetech-servo quadruped platform.

## Repository Layout

```text
.
|-- dog_feetch/                         Project-owned robot deployment code
|   |-- runtime/                        Runtime modules for inference, IMU, motor I/O, and keyboard control
|   |-- scripts/                        Calibration, diagnostics, RL walking, and open-loop walking scripts
|   |-- default_position.json           Default standing pose calibration
|   |-- imu_calib_data.pkl              IMU calibration data
|   |-- TEST.onnx                       Test policy/model artifact used by local scripts
|-- best.onnx                           Main ONNX policy artifact
|-- pypot-support-feetech-sts3215/      Vendor/third-party Feetech STS3215 support library
|-- Python-WitProtocol/                 Vendor/third-party WitMotion IMU protocol library
|-- README.md                           This project overview
```

## Third-Party Vendor Libraries

`pypot-support-feetech-sts3215` and `Python-WitProtocol` are vendor or third-party libraries. This project only imports and calls them to communicate with Feetech STS3215 servos and WitMotion IMU hardware. They are not treated as project-owned source code, and their internal source, comments, documentation, examples, build outputs, and metadata are intentionally left unchanged.

## Main Project Code

The project-owned code lives under `dog_feetch`.

### Runtime Modules

- `dog_feetch/runtime/position_hwi.py`: hardware interface for sending joint commands and reading servo feedback.
- `dog_feetch/runtime/onnx_infer.py`: ONNX Runtime wrapper for policy inference.
- `dog_feetch/runtime/raw_imu.py`: raw WitMotion IMU interface based on the vendor protocol library.
- `dog_feetch/runtime/horsebro_imu.py`: BNO08x IMU reader and quaternion-to-Euler conversion utility.
- `dog_feetch/runtime/rl_utils.py`: observation, filtering, and math utilities for learned policy deployment.
- `dog_feetch/runtime/xbox.py`: keyboard-backed controller interface compatible with the expected gamepad command shape.
- `dog_feetch/runtime/HWT_IMU_test.py`: WitMotion IMU diagnostic and logging script.

### Scripts

- `dog_feetch/scripts/walk_by_rl.py`: main real-robot learned-policy deployment loop.
- `dog_feetch/scripts/walk_by_openloop.py`: educational open-loop gait and inverse-kinematics walking controller.
- `dog_feetch/scripts/walk_by_openloop_leg_test.py`: single-leg or reduced-scope open-loop gait test.
- `dog_feetch/scripts/calibrate_joint_gui.py`: GUI tool for servo joint calibration.
- `dog_feetch/scripts/set_default_position.py`: records or updates the default standing pose.
- `dog_feetch/scripts/check_motor.py`: motor diagnostics and feedback inspection.
- `dog_feetch/scripts/configure_motor.py`: Feetech servo configuration helper.
- `dog_feetch/scripts/center_all_servos.py`: moves all configured servos toward the center position.
- `dog_feetch/scripts/test*.py` and `handmotor.py`: small local hardware test utilities.

## Typical Workflow

1. Install the vendor libraries or make sure their paths are available to Python.
2. Install runtime dependencies such as `numpy`, `onnxruntime`, `pyserial`, and hardware-specific packages required by the selected IMU and servo stack.
3. Connect the servo bus and IMU hardware.
4. Check serial device names and permissions. Most scripts default to Linux-style device paths such as `/dev/ttyUSB0`.
5. Run motor and IMU diagnostics before running a walking controller.
6. Start with calibration and low-power tests before using RL deployment.

## Example Commands

Run ONNX inference timing:

```bash
python dog_feetch/runtime/onnx_infer.py --onnx_model_path best.onnx
```

Run the learned-policy deployment loop:

```bash
python dog_feetch/scripts/walk_by_rl.py --onnx_model_path best.onnx --serial_port /dev/ttyUSB0
```

Run the educational open-loop controller:

```bash
python dog_feetch/scripts/walk_by_openloop.py --usb-port /dev/ttyUSB0
```

## Hardware Safety Notes

- Verify servo IDs, joint direction signs, and zero offsets before applying torque.
- Keep the robot physically supported during first tests.
- Use conservative `kp`, `kd`, action scale, and torque/current limits while debugging.
- Confirm IMU orientation and calibration data before using policy observations.
- Be ready to cut motor power if a joint moves in the wrong direction.

## Cleanup Policy

Generated Python caches such as `__pycache__` and `.pyc` files are not required for runtime and should not be committed. Vendor library directories are kept intact even if they contain their own build metadata.
