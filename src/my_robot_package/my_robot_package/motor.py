from pwm7046 import PWM7046
import time 
import math
import random

        
    
class dcmotdriver:
    def __init__(self, in1_pin, in2_pin, switch: bool = False):

        if switch:
            in1_pin, in2_pin = in2_pin, in1_pin

        self.mot1 = PWM7046(in1_pin, 800)
        self.mot2 = PWM7046(in2_pin, 800)
            
        self.mot1.value = 0  # start PWM with 0% duty cycle
        self.mot2.value = 0
        self.AXIS_ROTATION = 45 # deg

        

    def motgo(self, speed):
        pwm_value = abs(speed
                        ) #convert to%
        #print('speed pwm value = ', pwm_value)
        if speed > 0:
            self.mot1.value = pwm_value
            self.mot2.value = 0
        elif speed < 0:
            self.mot1.value = 0
            self.mot2.value = pwm_value
        else:
            self.mot1.value = 0
            self.mot2.value = 0    

    
    def stophard(self):
        self.mot1.value = 1
        self.mot2.value = 1

    def stop(self):
        self.mot1.value = 0
        self.mot2.value = 0
    
    def __del__(self):
        self.mot1.value = 0
        self.mot2.value = 0

    def calculate_speed(self, Vx, Vy, rotation):
        rad = math.radians(self.AXIS_ROTATION)
        cos = math.cos(rad)
        sin = math.sin(rad)
        
        # Standard 2D rotation matrix
        target_Vx = Vx * cos - Vy * sin
        target_Vy = Vx * sin + Vy * cos

        # 2. Combine components for each wheel
        # Each wheel gets a mix of Vx, Vy, and Rotation
        wheel1_speed = target_Vy + target_Vx + rotation # Front Left
        wheel2_speed = target_Vy - target_Vx - rotation # Front Right
        wheel3_speed = target_Vy - target_Vx + rotation # Rear Left
        wheel4_speed = target_Vy + target_Vx - rotation # Rear Right

        # 3. Normalization (Crucial!)
        # Since adding Vx + Vy + Rot can exceed 100, we must scale down
        speeds = [wheel1_speed, wheel2_speed, wheel3_speed, wheel4_speed]
        max_val = max(list(map(abs, speeds)) + [100])
        
        return [(s / max_val) * 100 for s in speeds]


if __name__ == "__main__":
    motor1 = dcmotdriver(19, 20, True) # green
    motor2 = dcmotdriver(21, 22) # white
    motor3 = dcmotdriver(23, 24, True) # orange
    motor4 = dcmotdriver(25, 26) # orange white
     
    # motor2.motgo(30)
    # motor3.motgo(100)
    motors: dcmotdriver = [motor3, motor1, motor2, motor4]
    speeds = motor1.calculate_speed(100, 0, 0)
    print(speeds)
    for i in range(len(speeds)):
        motors[i].motgo(speeds[i])
        

    input()

    del motor1, motor2, motor3, motor4

    
 