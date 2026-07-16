# coding:UTF-8
"""WitMotion JY901 IMU diagnostic and throttled logging script."""

import datetime
import platform
import time

import lib.device_model as deviceModel
from lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
from lib.protocol_resolver.roles.wit_protocol_resolver import WitProtocolResolver

welcome = """
WitMotion IMU diagnostic program.
Press Ctrl+C to stop streaming data.
"""
_writeF = None
_IsWriteF = False
last_print_time = 0


def readConfig(device):
    """Read selected device configuration registers."""
    tVals = device.readReg(0x02, 3)
    if len(tVals) > 0:
        print("0x02: " + str(tVals))
    else:
        print("0x02: no response")

    tVals = device.readReg(0x23, 2)
    if len(tVals) > 0:
        print("0x23: " + str(tVals))
    else:
        print("0x23: no response")


def setConfig(device):
    """Update the IMU output configuration and save it to the device."""
    device.unlock()
    time.sleep(0.1)
    device.writeReg(0x03, 6)  # 10 Hz output rate.
    time.sleep(0.1)
    device.writeReg(0x23, 0)
    time.sleep(0.1)
    device.writeReg(0x24, 0)
    time.sleep(0.1)
    device.save()


def AccelerationCalibration(device):
    """Run accelerometer calibration."""
    device.AccelerationCalibration()
    print("Accelerometer calibration complete.")


def FiledCalibration(device):
    """Run magnetometer calibration until the user confirms completion."""
    device.BeginFiledCalibration()
    if input("Finish three-axis magnetometer calibration? Enter Y: ").lower() == "y":
        device.EndFiledCalibration()
        print("Magnetometer calibration complete.")


def onUpdate(deviceModel):
    """Handle each IMU update and print at a throttled rate."""
    global last_print_time
    now = time.time()
    print_interval = 0.5

    if _IsWriteF:
        Tempstr = " " + str(deviceModel.getDeviceData("Chiptime"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("accX")) + "\t" + str(deviceModel.getDeviceData("accY")) + "\t" + str(deviceModel.getDeviceData("accZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("gyroX")) + "\t" + str(deviceModel.getDeviceData("gyroY")) + "\t" + str(deviceModel.getDeviceData("gyroZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("angleX")) + "\t" + str(deviceModel.getDeviceData("angleY")) + "\t" + str(deviceModel.getDeviceData("angleZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("temperature"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("magX")) + "\t" + str(deviceModel.getDeviceData("magY")) + "\t" + str(deviceModel.getDeviceData("magZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("lon")) + "\t" + str(deviceModel.getDeviceData("lat"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("Yaw")) + "\t" + str(deviceModel.getDeviceData("Speed"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q1")) + "\t" + str(deviceModel.getDeviceData("q2"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q3")) + "\t" + str(deviceModel.getDeviceData("q4"))
        Tempstr += "\r\n"
        _writeF.write(Tempstr)

    if now - last_print_time < print_interval:
        return
    last_print_time = now

    ax = round(deviceModel.getDeviceData("accX"), 2)
    ay = round(deviceModel.getDeviceData("accY"), 2)
    az = round(deviceModel.getDeviceData("accZ"), 2)
    roll = round(deviceModel.getDeviceData("angleX"), 2)
    pitch = round(deviceModel.getDeviceData("angleY"), 2)
    yaw = round(deviceModel.getDeviceData("angleZ"), 2)

    print(
        f"[Attitude] Roll:{roll:6.2f}deg Pitch:{pitch:6.2f}deg "
        f"Yaw:{yaw:6.2f}deg | Accel X:{ax:5.2f} Y:{ay:5.2f} Z:{az:5.2f}"
    )


def startRecord():
    """Start writing IMU samples to a timestamped text file."""
    global _writeF
    global _IsWriteF
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".txt"
    _writeF = open(filename, "w", encoding="utf-8")
    _IsWriteF = True
    header = "Chiptime\tax(g)\tay(g)\taz(g)\twx(deg/s)\twy(deg/s)\twz(deg/s)\tAngleX(deg)\tAngleY(deg)\tAngleZ(deg)\tT(C)\tmagx\tmagy\tmagz\tlon\tlat\tYaw\tSpeed\tq1\tq2\tq3\tq4\r\n"
    _writeF.write(header)
    print(f"Data logging enabled: {filename}")


def endRecord():
    """Stop IMU data logging."""
    global _writeF
    global _IsWriteF
    _IsWriteF = False
    _writeF.close()
    print("Data logging disabled.")


if __name__ == '__main__':
    print(welcome)
    device = deviceModel.DeviceModel(
        "JY901",
        WitProtocolResolver(),
        JY901SDataProcessor(),
        "51_0"
    )

    if platform.system().lower() == 'linux':
        device.serialConfig.portName = "/dev/ttyUSB0"
    else:
        device.serialConfig.portName = "COM17"
    device.serialConfig.baud = 921600

    device.openDevice()
    print("Serial port opened successfully.")
    readConfig(device)

    device.dataProcessor.onVarChanged.append(onUpdate)

    try:
        print("\nReading IMU data. Press Ctrl+C to stop.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping IMU test.")
        if _IsWriteF:
            endRecord()
        device.closeDevice()
        print("Device closed.")
