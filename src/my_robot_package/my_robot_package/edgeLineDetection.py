import motor
import data
from time import sleep
import gpiodIRQ

class EdgeLineDetection:
    def __init__(self):
        self.motors = motor.multipleMotors(data.MOTOR_PINS)
        self.leftIRQ = gpiodIRQ.GPIOD_IRQ(data.TCRT_PINS[0], self.escapeLeft, False)
        self.rightIRQ = gpiodIRQ.GPIOD_IRQ(data.TCRT_PINS[1], self.escapeRight, False)
        self.forwardIRQ = gpiodIRQ.GPIOD_IRQ(data.TCRT_PINS[2], self.escapeForward, False)

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
    e = EdgeLineDetection()
    
    while True:
        sleep(0.1)