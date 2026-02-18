import pwm7046
from time import sleep
import logging

s = pwm7046.PWM7046(12, 50)

class Servo:
    def __init__(self, pin: int, chipID: int = 0):
        self.FREQ = 50

        self.servoAngle = 0

        self.servo = pwm7046.PWM7046(pin, self.FREQ, chipID)

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    @staticmethod
    def calculateDuty(angle: int):
        return 2.5 + (angle / 180) * 10
    
    @property
    def angle(self):
        return self.servoAngle

    @angle.setter
    def angle(self, angle: int):
        if (angle < 0 or angle > 180):
            self.log.error("Error: angle must be between 0 and 180")
            raise Exception("Error: angle must be between 0 and 180")

        duty = Servo.calculateDuty(angle)
        self.servo.value = duty

        self.log.debug(f"Changed angle to {angle} in duty {duty}")
        print(f"Changed angle to {angle} in duty {duty}")

        sleep(0.5)
        self.servo.value = 0

if __name__ == "__main__":
    s = Servo(6)
    while True:
        angle = input("Enter angle (0-180) or 'q' to quit: ")
        if angle == 'q': break
        
        angle = float(angle)
        s.angle = angle