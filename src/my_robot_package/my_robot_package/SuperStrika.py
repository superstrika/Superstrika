from motor import Motor
import time

class SuperStrika:
    def __init__(self):
        # Initialize four motors
        self.m1 = Motor(26, 25)
        self.m2 = Motor(23, 24)
        self.m3 = Motor(22, 21)
        self.m4 = Motor(20, 19)

    def forward(self, speed=1023):
        """
        Move all motors forward at given speed.
        """
        # self.m1.startMotor(True, speed)
        # self.m2.startMotor(True, speed)
        # self.m3.startMotor(True, speed)
        # self.m4.startMotor(True, speed)
        print("All motors moving forward!")

    def stop(self):
        """
        Stop all motors.
        """
        self.m1.stopMotor()
        self.m2.stopMotor()
        self.m3.stopMotor()
        self.m4.stopMotor()

    def main(self, speed=1023):
        """
        Run forward indefinitely (no PID).
        """
        try:
            print(f"Moving forward at speed {speed}...")
            self.forward(speed)
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Stopping motors...")
            self.stop()

if __name__ == "__main__":
    robot = SuperStrika()
    robot.main(speed=600)
