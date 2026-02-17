from pwm7046 import PWM7046
from time import sleep
class Servo7046:

    def __init__(self, pin, limits: tuple = (0, 500), chipID=0):
        self._pwm = PWM7046(pin, freq=50, chipID=chipID)   # 50Hz for servo
        self._min_angle = limits[0]
        self._max_angle = 500

        self._min_duty = 2.5
        self._max_duty = 50

    def move(self, angle):
        # Limit angle
        if angle < self._min_angle:
            angle = self._min_angle
        if angle > self._max_angle:
            angle = self._max_angle

        # Convert angle to duty cycle
        duty = self._min_duty + (
            (angle - self._min_angle) /
            (self._max_angle - self._min_angle)
        ) * (self._max_duty - self._min_duty)

        self._pwm.value = duty
if __name__ == "__main__":
    servo = Servo7046(2)
    servo.move(500)
    sleep(1)
    servo.move(0)