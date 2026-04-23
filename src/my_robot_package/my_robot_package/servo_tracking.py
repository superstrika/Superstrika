from time import sleep
import servo
import data

class servoTracking:

    def __init__(self, parent: Hunt):
        if not parent or not parent.servo or not parent.trackingLock:
            raise Exception("Servo Tracking: Parent class doesn't exists or does not contain servo / lock")
        
        self.parent = parent

    def track(self):
        with self.parent.servoCondition:
            while self.parent.


if __name__ == "__main__":
    cal = servoTracking(data.SERVO_PIN, True)
