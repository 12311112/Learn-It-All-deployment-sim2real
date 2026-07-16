# dog_feetch

`dog_feetch` contains the project-owned real-robot deployment code for the Feetech-servo quadruped platform.

- `runtime/` provides reusable modules for motor I/O, IMU access, ONNX inference, filtering, and command input.
- `scripts/` contains calibration, diagnostics, open-loop gait, and learned-policy deployment entry points.
- `default_position.json` stores the calibrated default standing pose.
- `imu_calib_data.pkl` stores local IMU calibration data.
- `TEST.onnx` is a local ONNX model artifact used by project scripts.

See the repository-level `README.md` for setup, vendor-library, and hardware-safety notes.
