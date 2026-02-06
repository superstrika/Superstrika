from pwm7046 import PWM7046
import math
    
class motor7046:
    _h = 0

    def __init__(self, pin1, pin2, switch: bool = False, chipID: int = 0):

        if switch:
            print("hi")
            pin1, pin2 = pin2, pin1

        self.mot1 = PWM7046(pin1, 800)
        self.mot2 = PWM7046(pin2, 800)

        self._speed = 0
        self.mot1.value = 0  # start PWM with 0% duty cycle
        self.mot2.value = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
        pwm_value = abs(self._speed)

        if self._speed > 0:
            self.mot1.value = pwm_value
            self.mot2.value = 0
        elif self._speed < 0:
            self.mot1.value = 0
            self.mot2.value = pwm_value
        else:
            self.mot1.value = 0
            self.mot2.value = 0

    def stophard(self):
        self._speed = 100
        self.mot1.value = 100
        self.mot2.value = 100

    def stop(self):
        self._speed = 0
        self.mot1.value = 0
        self.mot2.value = 0

    def __del__(self):
        self._speed = 0
        self.mot1.value = 0
        self.mot2.value = 0

    @staticmethod
    def calculate_speed(Vx, Vy, rotation):
        AXIS_ROTATION = -45
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
        wheel3_speed = rotatedVy - rotation  # Rear Right
        wheel4_speed = rotatedVx + rotation  # Rear Left

        # 3. Normalization (Scaling)
        # This ensures that if the math results in '141', it scales back to '100'
        speeds = [wheel1_speed, wheel2_speed, wheel3_speed, wheel4_speed]
        max_val = max(list(map(abs, speeds)) + [100])

        return [(i if abs(i) > 1 else 0) for i in [(s / max_val) * 100 for s in speeds]]
    
    def calculate_rotation_speed(speed):
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        return [speed for i in range(4)] # [speed, speed, speed, speed] 

class multipleMotors:
    def __init__(self, pins: list[int]):
        motor1 = motor7046(pins[0], pins[1], switch=True) # green
        motor2 = motor7046(pins[2], pins[3], switch=False) # white
        motor3 = motor7046(pins[4], pins[5], switch=False) # orange
        motor4 = motor7046(pins[6], pins[7], switch=True) # orange

        self.motors: list[motor7046] = [motor1, motor2, motor3, motor4]
    
    def setSpeedVxVy(self, Vx, Vy):
        self.motors[0].speed = Vx
        self.motors[1].speed = Vx
        self.motors[2].speed = Vy
        self.motors[3].speed = Vy

    def setSpeed(self, V1, V2, V3, V4):
        self.motors[0].speed = V1
        self.motors[1].speed = V2
        self.motors[2].speed = V3
        self.motors[3].speed = V4

if __name__ == "__main__":
    motor1 = motor7046(19, 20, switch=False) # green
    motor2 = motor7046(21, 22, switch=False) # white
    motor3 = motor7046(23, 24, switch=True) # orange
    motor4 = motor7046(25, 6, switch=True) # orange

    # motor3.speed = -100

    motors: motor7046 = [motor1, motor2, motor3, motor4]
    speeds = motor1.calculate_speed(0, 70, 0)
    print(speeds)
    for i in range(len(speeds)):
        motors[i].speed = speeds[i]
        

    input()

    del motor1, motor2, motor3, motor4

    # motor = motor7046(25, 6, switch=False)
    # motor.speed = -100
    # input()
    # del motor
    
 