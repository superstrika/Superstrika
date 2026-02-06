from yellow_motor import yellowMotor7046
from time import sleep

class Kicker:
    GEAR_TEETH = 4

    def __init__(self, pin1, pin2):
        self.motor = yellowMotor7046(pin1, pin2)

    def loadPoint(self, speed=55):
        self.motor.speed = speed
        
    def load(self, p: int):
        for i in range(Kicker.GEAR_TEETH):
            self.motor.speed = i * p
            sleep(i*1.1 + 0.1)
    def release(self, pin1, pin2):
        print("Releasing")
        self.motor.speed = -100
        sleep(0.5)
        self.motor.speed = 0

if __name__ == "__main__":
    kicker = Kicker(27, 13)
    kicker.loadPoint()
    sleep(1)
    kicker.load(50.45)
    kicker.release(27, 26)
