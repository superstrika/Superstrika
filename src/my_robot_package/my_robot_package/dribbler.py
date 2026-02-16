import motor

def dribbler_test():
    dribbler = motor.motor7046(17, 18)  # Example GPIO pins
    dribbler.speed = 100
    input("Dribbler running at full speed. Press Enter to stop.")
    dribbler.speed = 0  # Stop the dribbler

if __name__ == "__main__":
    dribbler_test()