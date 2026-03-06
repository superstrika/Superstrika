import motor
import data

class Dribbler:
    def __init__(self, pins: list[int], chipID: int = 0):
        self.dribbler = motor.motor7046(pins[0], pins[1], chipID=chipID)

    def turn_on(self, speed: int = 100):
        self.dribbler.speed = speed

    def turn_off(self):
        self.dribbler.speed = 0

def dribbler_test():
    dribbler = motor.motor7046(13, 16)  # Example GPIO pins
    dribbler.speed = -100
    input("Dribbler running at full speed. Press Enter to stop.")
    dribbler.speed = 0  # Stop the dribbler

if __name__ == "__main__":
    dribbler_test()