from yellow_motor import yellowMotor7046
from time import sleep

class Kicker:
    GEAR_TEETH = 7

    def __init__(self, pin1, pin2):
        self.motor = yellowMotor7046(pin1, pin2)

    def kick(self, p: int):
        for i in range(Kicker.GEAR_TEETH):
            self.motor.speed = i * p
            sleep(0.1)
        sleep(0.1)
        self.motor.speed = 0

if __name__ == "__main__":
    kicker = Kicker(12, 13)
    kicker.kick(1)
