import argparse
import sys

from . import args
import robot.consts.data as data
from robot.consts.enum import *
from robot.calibration import *
from robot.components import *
from robot.processes import *

from smbus2 import SMBus as I2C
import gpiozero

from time import time, sleep
import math
import logging

logging.basicConfig(filename=data.LOG_PATH, filemode='w', level=logging.DEBUG, format=data.LOG_FORMAT)

class Hunter:
    def __init__(self, args: argparse.Namespace):
        self._i2c = I2C(args.i2c)

        self._servo = servo.Servo(data.SERVO_PIN)
        self._servo.angle = data.MAX_ANGLE

        self._gyro = gyro.MPU6050(self._i2c)

        self._motors = MultipleMotors.MultipleMotors(data.MOTOR_PINS)
        self._dribbler = dribbler.Dribbler(data.DRIBBLER_PIN)
        self._kicker = kicker.Kicker(data.KICKER_PIN)

        self._camera = webcamera.WebCamera(
            f"/home/admin/Superstrika/robot/models/best-V{args.modelVersion}.onnx",
            focalLength=194.487,
            cameraIndex=args.cameraIndex,
            showLiveFeed=args.showLiveFeed,
            saveFrames=args.saveFrames,
        )

        self._gyroMovement = gyroMovement.GyroMovement(self._i2c, self._gyro, self._motors)

        self._log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

        if args.debug:
            consoleHandler = logging.StreamHandler(sys.stdout)
            consoleHandler.setFormatter(logging.Formatter(data.LOG_FORMAT))
            self._log.logger.addHandler(consoleHandler)

    def cameraSearch(self, obj: Object = Object.Ball) -> bool:
        self._log.info("Started Camera Search")

        for angle in [data.MAX_ANGLE, data.MID_ANGLE, data.MIN_ANGLE]:
            self._servo.angle = angle
            sleep(0.1)
            if self._camera.isObjectDetected(obj):
                return True

        return False

    def spinSearch(self, obj: Object = Object.Ball) -> bool:
        self._log.info("Started Spin Search")

        angle = startAngle = self._gyro.get_z_angle()
        while abs(angle - startAngle) < 360:
            detectedObject = self._camera.getObjects()

            if detectedObject[obj]:
                self._log.info(f"Object detected: {obj.name}")
                return True

            if obj == Object.Ball:
                if self.cameraSearch(obj):
                    return True

            self._gyroMovement.spinToAngle(angle + 45)
            angle = self._gyro.get_z_angle()

        self._log.info(f"Object not detected: {obj.name}")
        return False

    def goToObject(self, obj: Object = Object.Ball) -> bool:
        self._log.info(f"Started Going to: {obj.name}")

        target = data.BALL_IN_KICKER_DISTANCE if obj == Object.Ball else data.ROBOT_GOAl_DISTANCE

        pidAngle = pidCalc.PidCalc(0.4, 0.2, 0, 100)
        pidDist = pidCalc.PidCalc(2.5, 0, 0.1, 100/math.cos(math.radians(data.MOTOR_CROSS_ANGLE)))

        error = self._camera.getObjects()[obj]
        while error:
            if error.distance - target < data.BALL_IN_KICKER_DISTANCE:
                self._log.info(f"Found Object: {obj.name}")
                self._motors.stophard()
                return True

            correction = pidAngle.pidCalc(-error.angle)
            speedY = max(pidDist.pidCalc(error.distance - target), data.GO_TO_BALL_MIN_SPEED)

            self._motors.setSpeed(0, speedY, correction)

            error = self._camera.getObjects()[obj]

        self._motors.stophard()
        return False

    def hunt(self):
        while True:
            status = self._camera.getObjectsStatus()[Object.Ball]

            if status == BallStatus.CAM_DETECTED:
                self._log.info("Ball Detected!")
                if self.goToObject(Object.Ball):
                    input("Got to Ball!")

            if status == BallStatus.NOT_FOUND:
                self._log.info("Ball Not Found!")
                if not self.spinSearch(Object.Ball):
                    input("Spin Search Failed!")

if __name__ == "__main__":
    h = Hunter(args)
    h.hunt()