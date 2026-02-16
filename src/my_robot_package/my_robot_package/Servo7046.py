from pwm7046 import PWM7046

class Servo7046:

    def __init__(self, pin, limits: tuple = (0, 180), chipID=0):
        self._pwm = PWM7046(pin, freq=50, chipID=chipID)   # 50Hz for servo
        self._min_angle = limits[0]
        self._max_angle = limits[1]

        self._min_duty = 2.5
        self._max_duty = 12.5

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