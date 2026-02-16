import motor
import data
from time import sleep

class EdgeLineDetection:
    def __init__(self):
        self.motors = motor.multipleMotors(data.MOTOR_PINS)

    def escapeLeft(self):
        self.motors.setSpeedVxVy(-100, 0)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeRight(self):
        self.motors.setSpeedVxVy(100, 0)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeForward(self):
        self.motors.setSpeedVxVy(0, 100)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

if __name__ == "__main__":
    e = EdgeLineDetection
    e.escapeLeft()
    