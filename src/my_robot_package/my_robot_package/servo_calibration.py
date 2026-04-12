from time import sleep
import servo
import data

class servoCalibration:

    def __init__(self, servo_: int | servo.Servo, auto_calibrate: bool = False):
        if type(servo_) == type(servo.Servo):
            self._servo = servo_
        else:
            self._servo = servo.Servo(servo_)
        
        self.MIN_ANGLE = 85
        self.MAX_ANGLE = 180

        if auto_calibrate:
            self.calibrate()

    def calibrate(self):
        input("Press enter to start the callibration...")
        self._servo.angle = self.MIN_ANGLE

        print(f"Moving servo to {self.MIN_ANGLE} deg. Move the camera to the desired position.")

        input("To continue press enter...")
        self._servo.angle = self.MAX_ANGLE

        print(f"Moving servo to {self.MAX_ANGLE} deg. Make sure this is the desired \"max\" position.")

        print("Enter 'y' to repeat.")
        chr = input()

        if chr == 'y':
            self.calibrate()

if __name__ == "__main__":
    cal = servoCalibration(data.SERVO_PIN, True)
    # cal.calibrate()