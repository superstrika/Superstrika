from pwm7046 import PWM7046
import time 
import math
import random

        
    
class dcmotdriver:
    def __init__(self, in1_pin, in2_pin):
        self.mot1 = PWM7046(in1_pin, 800)
        self.mot2 = PWM7046(in2_pin, 800)
        self.mot1.value = 0  # start PWM with 0% duty cycle
        self.mot2.value = 0
        

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


if __name__ == "__main__":
    motor1 = dcmotdriver(19, 20)
    motor2 = dcmotdriver(21, 22)
    motor3 = dcmotdriver(23, 24)
    motor4 = dcmotdriver(25, 26)
     
    motor2.motgo(30)
    motor1.motgo(-30)

    input()

    del motor, motor2, motor3, motor4

    
 