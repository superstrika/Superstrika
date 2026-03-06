from pidCalc import PidCalc
from gyro import MPU6050
from motor import multipleMotors, motor7046
from smbus2 import SMBus as I2C  # For RPI compatibility
from time import sleep
import data

class GyroMovement:
    
    def __init__(self, i2c: I2C = None, gyro: MPU6050 = None, motors: multipleMotors = None, pidValues: list[float] = [0.35, 0.15, 0.01, 10, 100, 100], errorOffset: float = 0.5):
        if i2c and not gyro:
            self.i2c = i2c
            self.gyro = MPU6050(self.i2c)
        elif not gyro:
            self.i2c = I2C(1)
            self.gyro = MPU6050(self.i2c)
        else :
            self.i2c = None
            self.gyro = gyro

        if motors:
            self.motors = motors
        else:
            self.motors = multipleMotors(data.MOTOR_PINS)

        self._pidYaw = PidCalc(*tuple(pidValues))
        self._errorOffset = errorOffset

    def spinToAngle(self, setPoint: int) -> None:
        error: float = setPoint - self.gyro.get_z_angle()

        while abs(error) > self._errorOffset:
            speed: float = self._pidYaw.pidCalc(error)

            if speed > 10 and speed < 30:
                speed += 20
            
            if speed < -10 and speed > -30:
                speed -= 20

            speeds: list[int] = motor7046.calculate_rotation_speed(speed)
            self.motors.setSpeed(speeds[0], speeds[1], speeds[2], speeds[3])

            sleep(0.3)
            error: float = setPoint - self.gyro.get_z_angle()

if __name__ == "__main__":
    mov = GyroMovement(1)
    mov.spinToAngle(90)
