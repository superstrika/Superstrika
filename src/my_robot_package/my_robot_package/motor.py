from pwm7046 import PWM7046
import math
import logging
import data
    
class motor7046:
    _h = 0
    MIN_SPEED = 30

    def __init__(self, pin1, pin2, switch: bool = False, chipID: int = 0, verbose: bool = True):

        if switch:
            print("hi")
            pin1, pin2 = pin2, pin1

        self.mot1 = PWM7046(pin1, 800, verbose=verbose)
        self.mot2 = PWM7046(pin2, 800, verbose=verbose)

        self._speed = 0
        self.mot1.value = 0  # start PWM with 0% duty cycle
        self.mot2.value = 0

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

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

        self.log.debug(f"Motor speed is now: {speed}")

    def stophard(self):
        self._speed = 100
        self.mot1.value = 100
        self.mot2.value = 100
        self.log.debug(f"Stopped hard!")

    def stop(self):
        self._speed = 0
        self.mot1.value = 0
        self.mot2.value = 0
        self.log.debug(f"Motor speed is now: 0")

    def __del__(self):
        self._speed = 0
        self.mot1.value = 0
        self.mot2.value = 0

    @staticmethod
    def calculate_speed(Vx, Vy, rotation):
        # AXIS_ROTATION = -45
        # Vx, Vy = Vy, Vx # if motors swaps
        # Vy = -Vy
        # rad = math.radians(AXIS_ROTATION)  # Or self.AXIS_ROTATION
        # cos = math.cos(rad)
        # sin = math.sin(rad)

        # Standard rotation matrix to find the 'Wheel-Aligned' components
        # rotatedVx = Vx * cos - Vy * sin
        # rotatedVy = Vx * sin + Vy * cos
        # rotatedVx = Vy * cos - Vx * sin
        # rotatedVy = Vy * sin + Vx * cos

        # 2. Assign to wheels based on the X-pattern
        # In an X-drive, the diagonal pairs handle the rotated vectors
        # wheel1_speed = rotatedVx - rotation  # Front Right
        # wheel2_speed = rotatedVx + rotation  # Rear Left
        # wheel3_speed = rotatedVy + rotation  # Front Left
        # wheel4_speed = rotatedVy - rotation  # Rear Right
        # wheel1_speed = rotatedVx + rotation
        # wheel2_speed = rotatedVy - rotation
        # wheel3_speed = rotatedVy + rotation 
        # wheel4_speed = rotatedVx - rotation 

        # 3. Normalization (Scaling)
        # This ensures that if the math results in '141', it scales back to '100'
        # speeds = [wheel1_speed, wheel2_speed, wheel3_speed, wheel4_speed]
        # max_val = max(list(map(abs, speeds)) + [100])

        # return [(i if abs(i) > 1 else 0) for i in [(s / max_val) * 100 for s in speeds]]

        # Front Left
        wheel1_speed = Vy - Vx + rotation
        # Front Right
        wheel2_speed = Vx + Vy - rotation
        # Rear Left
        wheel3_speed = Vx - Vy + rotation
        # Rear Right
        wheel4_speed = -Vx - Vy - rotation

        # 2. Collect speeds
        speeds = [wheel1_speed, wheel2_speed, wheel3_speed, wheel4_speed]

        # 3. Normalization (Scaling)
        # This prevents values from exceeding your motor limits (e.g., 100)
        # while maintaining the ratio of movement.
        max_val = max(list(map(abs, speeds)) + [100])
        
        normalized_speeds = [(s / max_val) * 100 for s in speeds]

        # 4. Deadband check (ignore very small values to save motor life)
        return [(i if abs(i) > 1 else 0) for i in normalized_speeds]

    @staticmethod
    def calculate_rotation_speed(speed):
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        return [-speed for i in range(4)] # [speed, speed, speed, speed] 

class multipleMotors:
    def __init__(self, pins: list[int], chipID: int = 0, verbose: bool = True, speedVerbose: bool = False, parent = None):

        self.parent = parent

        if speedVerbose == True:
            verbose = False
        self.speedVerbose = speedVerbose

        motor1 = motor7046(pins[0], pins[1], switch=False, chipID=chipID, verbose=verbose)
        motor2 = motor7046(pins[2], pins[3], switch=False, chipID=chipID, verbose=verbose)
        motor3 = motor7046(pins[4], pins[5], switch=True, chipID=chipID, verbose=verbose)
        motor4 = motor7046(pins[6], pins[7], switch=True, chipID=chipID, verbose=verbose)

        self.motors: list[motor7046] = [motor1, motor2, motor3, motor4]
    
    def stop(self):
        self.setSpeed(0, 0, 0, 0)

    def setSpeed(self, V1, V2, V3, V4):

        if self.parent:
            with self.parent.condition:
                while self.parent.priority_active:
                    print("Waiting for interupt...")
                    self.parent.condition.wait()
            
                if self.speedVerbose:
                    print(f"V1: {V1}. V2: {V2}. V3: {V3}. V4: {V4}")
                self.motors[0].speed = V1
                self.motors[1].speed = V2
                self.motors[2].speed = V3
                self.motors[3].speed = V4
        else:
            if self.speedVerbose:
                print(f"V1: {V1}. V2: {V2}. V3: {V3}. V4: {V4}")
            self.motors[0].speed = V1
            self.motors[1].speed = V2
            self.motors[2].speed = V3
            self.motors[3].speed = V4

if __name__ == "__main__":
    # motor1 = motor7046(19, 20, switch=False) # green
    # motor2 = motor7046(21, 22, switch=False) # white
    # motor3 = motor7046(23, 24, switch=True) # orange
    # motor4 = motor7046(25, 6, switch=True) # orange

    # # motor3.speed = -100

    # motors: motor7046 = [motor1, motor2, motor3, motor4]
    # speeds = motor1.calculate_speed(0, 70, 0)
    # print(speeds)
    # for i in range(len(speeds)):
    #     motors[i].speed = speeds[i]
        

    # input()

    # del motor1, motor2, motor3, motor4

    # motor = motor7046(25, 6, switch=False)
    # motor.speed = -100
    # input()
    # del motor

    motors = multipleMotors(data.MOTOR_PINS)
    speeds = motor7046.calculate_speed(60, 0, 0)
    print(speeds)
    motors.setSpeed(*(tuple(speeds)))

    input()

    motors.stop()
    
 