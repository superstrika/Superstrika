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
        pwm_value = speed #convert to%
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

if __name__ == "__main__":
     motor = dcmotdriver(19, 20)
     motor2 = dcmotdriver(22, 23)
     motor.motgo(100)
     motor2.motgo(100)

    
