import machine
import math
    
class yellowMotor7046:

    def __init__(self, pin1, pin2, switch: bool = False):

        if switch:
            pin1, pin2 = pin2, pin1

        self.mot1 = machine.PWM(machine.Pin(pin1))
        self.mot2 = machine.PWM(machine.Pin(pin2))

        self._speed = 0
        self.mot1.duty_u16(0)  # start PWM with 0% duty cycle
        self.mot2.duty_u16(0)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
        pwm_value = abs(self._speed)
        pwm_value = map(pwm_value, 0, 100, 0, 65535)

        if self._speed > 0:
            self.mot1.duty_u16(pwm_value)
            self.mot2.duty_u16(0)
        elif self._speed < 0:
            self.mot1.duty_u16(0)
            self.mot2.duty_u16(pwm_value)
        else:
            self.mot1.duty_u16(0)
            self.mot2.duty_u16(0)

    def stophard(self):
        self._speed = 1
        self.mot1.duty_u16(1)
        self.mot2.duty_u16(1)

    def stop(self):
        self._speed = 0
        self.mot1.duty_u16(0)
        self.mot2.duty_u16(0)

    def __del__(self):
        self._speed = 0
        self.mot1.duty_u16(0)
        self.mot2.duty_u16(0)


    @staticmethod
    def calculate_speed(Vx, Vy, rotation):
        Vx = -Vx
        AXIS_ROTATION = 45
        rad = math.radians(AXIS_ROTATION)  # Or self.AXIS_ROTATION
        cos = math.cos(rad)
        sin = math.sin(rad)

        # Standard rotation matrix to find the 'Wheel-Aligned' components
        rotatedVx = Vx * cos - Vy * sin
        rotatedVy = Vx * sin + Vy * cos

        # 2. Assign to wheels based on the X-pattern
        # In an X-drive, the diagonal pairs handle the rotated vectors
        wheel1_speed = rotatedVy + rotation  # Front Left
        wheel2_speed = rotatedVx - rotation  # Front Right
        wheel3_speed = rotatedVx + rotation  # Rear Left
        wheel4_speed = rotatedVy - rotation  # Rear Right

        # 3. Normalization (Scaling)
        # This ensures that if the math results in '141', it scales back to '100'
        speeds = [wheel1_speed, wheel2_speed, wheel3_speed, wheel4_speed]
        max_val = max(list(map(abs, speeds)) + [100])

        return [(s / max_val) * 100 for s in speeds]


if __name__ == "__main__":
    pass

    
 