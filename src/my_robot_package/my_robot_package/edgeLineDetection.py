import motor
import data
from time import sleep
import gpiodIRQ
import logging

class EdgeLineDetection:
    def __init__(self, pins: list[int], chipID: int = 0):
        self.motors = motor.multipleMotors(data.MOTOR_PINS)
        self.leftIRQ = gpiodIRQ.GPIOD_IRQ(pins[0], self.escapeLeft, False, chipID=chipID)
        self.rightIRQ = gpiodIRQ.GPIOD_IRQ(pins[1], self.escapeRight, False, chipID=chipID)
        self.forwardIRQ = gpiodIRQ.GPIOD_IRQ(pins[2], self.escapeForward, False, chipID=chipID)

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def escapeLeft(self):
        print(f"Escaping left: {data.TCRT_PINS[0]}")
        speeds = motor.motor7046.calculate_speed(-100, 0, 0)
        self.motors.setSpeed(*(tuple(speeds)))

        print("Escaping left!")
        self.log.warning("Escaping left!")

        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeRight(self):
        print(f"Escaping right: {data.TCRT_PINS[1]}")
        speeds = motor.motor7046.calculate_speed(100, 0, 0)
        self.motors.setSpeed(*(tuple(speeds)))
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

    def escapeForward(self):
        print(f"Escaping forward: {data.TCRT_PINS[2]}")
        speeds = motor.motor7046.calculate_speed(0, 100, 0)
        self.motors.setSpeed(*(tuple(speeds)))
        sleep(0.1)
        self.motors.setSpeedVxVy(0, 0)

if __name__ == "__main__":
    e = EdgeLineDetection(data.TCRT_PINS)
    
    while True:
        sleep(0.1)