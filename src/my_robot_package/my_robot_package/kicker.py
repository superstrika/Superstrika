import motor
from time import sleep

class Kicker:
    # GEAR_TEETH = 4
    GEAR_TEETH = 3

    def __init__(self, pin1, pin2):
        self.motor = motor.motor7046(pin1, pin2, switch=True)
        motor.speed = 0

    def loadPoint(self, speed=55):
        self.motor.speed = speed
        
    def load(self, p: int):
        print("Loading..")
        for i in range(1, Kicker.GEAR_TEETH):
            if (i * p > 100):
                self.motor.speed = 100
            else:
                self.motor.speed = i * p
            sleep(5 / (i * p))
        self.motor.stophard()
        input()

    def release(self):
        print("Releasing")
        self.motor.speed = 100
        sleep(0.005)
        self.motor.speed = 0

if __name__ == "__main__":
    kicker = Kicker(12, 13)
    kicker.loadPoint(43)
    sleep(0.25)
    kicker.load(50.45)
    # kicker.release()
