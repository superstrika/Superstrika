import pwm7046
from time import sleep

s = pwm7046.PWM7046(12, 50)

class Servo:
    def __init__(self, pin: int):
        self.FREQ = 50

        self.servoAngle = 0

        self.servo = pwm7046.PWM7046(pin, self.FREQ)

    @staticmethod
    def calculateDuty(angle: int):
        return 2.5 + (angle / 180) * 10
    
    @property
    def angle(self):
        return self.servoAngle

    @angle.setter
    def angle(self, angle: int):
        if (angle < 0 or angle > 180):
            raise Exception("Error: angle must be between 0 and 180")

        duty = Servo.calculateDuty(angle)
        print(f"Hardware updated: Servo is now at angle: {angle} in duty {duty}")
        self.servo.value = duty
        sleep(0.5)
        self.servo.value = 0

if __name__ == "__main__":
    s = Servo(6)
    while True:
        angle = input("Enter angle (0-180) or 'q' to quit: ")
        if angle == 'q': break
        
        angle = float(angle)
        s.angle = angle