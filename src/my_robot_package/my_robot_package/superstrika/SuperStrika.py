# SuperStrika.py

from motor import Motor
from Gyro import MPU6050
import smbus
import time



class SuperStrika:
    def __init__(self, bus_num=1, mpu_addr=0x68):
        # Initialize four motors
        self.m1 = Motor(26, 25) 
        self.m2 = Motor(23, 24) 
        self.m3 = Motor(22, 21) 
        self.m4 = Motor(20, 19) 
        
        # Initialize I2C bus and MPU6050
        self.bus = smbus.SMBus(bus_num)
        self.MPU = MPU6050(self.bus, mpu_addr)
        self.MPU.reset_theta()  # Start from zero

        # PID internal states
        self._integral = 0
        self._last_error = 0
        self._last_time = time.time()

    def calc(self, Sp, Pv, Kp, Ki, Kd):
        error = Sp - Pv
        current_time = time.time()
        dt = current_time - self._last_time if self._last_time else 1.0

        self._integral += error * dt
        derivative = (error - self._last_error) / dt if dt > 0 else 0
        output = Kp * error + Ki * self._integral + Kd * derivative

        self._last_error = error
        self._last_time = current_time

        return output

    def get_yaw(self):
        """
        Returns the yaw (Z-axis rotation) in degrees from MPU6050.
        """
        theta = self.MPU.get_theta()
        return theta['z']

    def main(self, speed=100):
        while True:
            self.m1.startMotor(True, speed)
            # self.m2.startMotor(True, speed)
            # self.m3.startMotor(True, speed)
            # self.m4.startMotor(True, speed)

robot = SuperStrika()
robot.main(speed=1023)  # Example usage with speed set to 100


