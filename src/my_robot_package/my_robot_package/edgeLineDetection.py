import motor
import data
from time import sleep
import gpiodIRQ
import logging
import threading

class EdgeLineDetection:
    def __init__(self, pins: list[int], chipID: int = 0, motors: motor.multipleMotors = None, parent = None):
        if motors:
            self.motors = motors
        else:
            self.motors = motor.multipleMotors(data.MOTOR_PINS)

        self.leftIRQ = gpiodIRQ.GPIOD_IRQ(pins[0], self.escapeLeft, False, chipID=chipID)
        self.rightIRQ = gpiodIRQ.GPIOD_IRQ(pins[1], self.escapeRight, False, chipID=chipID)
        self.forwardIRQ = gpiodIRQ.GPIOD_IRQ(pins[2], self.escapeForward, False, chipID=chipID)

        if not parent:
            raise Exception("This process is an orphan :(")
        self.parent = parent

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def escapeLeft(self):
        print(f"Escaping left: {data.TCRT_PINS[0]}")
        speeds = motor.motor7046.calculate_speed(-100, 0, 0)

        with self.parent.condition:
            self.parent.priority_active = True

            self.motors.setSpeed(*(tuple(speeds)))
            self.log.warning("Escaping left!")
            sleep(0.15)
            self.motors.setSpeedVxVy(0, 0)

            self.parent.priority_active = False
            self.parent.condition.notify_all()

    def escapeRight(self):
        print(f"Escaping right: {data.TCRT_PINS[1]}")
        speeds = motor.motor7046.calculate_speed(100, 0, 0)
        
        with self.parent.condition:
            self.parent.priority_active = True

            self.motors.setSpeed(*(tuple(speeds)))
            self.log.warning("Escaping right!")
            sleep(0.15)
            self.motors.setSpeedVxVy(0, 0)

            self.parent.priority_active = False
            self.parent.condition.notify_all()

    def escapeForward(self):
        print(f"Escaping forward: {data.TCRT_PINS[2]}")
        speeds = motor.motor7046.calculate_speed(0, 100, 0)

        with self.parent.condition:
            self.parent.priority_active = True

            self.motors.setSpeed(*(tuple(speeds)))
            self.log.warning("Escaping Forward!")
            sleep(0.15)
            self.motors.setSpeedVxVy(0, 0)

            self.parent.priority_active = False
            self.parent.condition.notify_all()

if __name__ == "__main__":
    e = EdgeLineDetection(data.TCRT_PINS)
    
    while True:
        sleep(0.1)