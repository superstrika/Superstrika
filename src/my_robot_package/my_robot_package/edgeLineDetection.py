import motor
import data
from time import sleep
import lgpioIRQ

class EdgeLineDetection:
    def __init__(self):
        self.motors = motor.multipleMotors(data.MOTOR_PINS)
        self.irq = lgpioIRQ.IRQ(data.TCRT_PINS, [self.escapeLeft, self.escapeRight, self.escapeForward])

    def escapeLeft(self):
        print("Escaping left!")
        self.motors.setSpeedVxVy(-100, 0)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeRight(self):
        print("Escaping right!")
        self.motors.setSpeedVxVy(100, 0)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeForward(self):
        print("Escaping forward!")
        self.motors.setSpeedVxVy(0, 100)
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

if __name__ == "__main__":
    e = EdgeLineDetection
    e.escapeLeft()
    