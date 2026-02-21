from pidCalc import PidCalc
from gyro import MPU6050
from motor import multipleMotors, motor7046
from smbus2 import SMBus as I2C  # For RPI compatibility
from time import sleep
import data

class GyroMovement:
    
    def __init__(self, errorOffset: float = 0.5):
        self._i2c = I2C(1)
        self._gyro = MPU6050(self._i2c)

        self.motors = multipleMotors(data.MOTOR_PINS)
        self._pidYaw = PidCalc(0.35, 0.15, 0.01, 10, 100, 100)
        self._errorOffset = errorOffset

    @staticmethod
    def getYaw(gyro: MPU6050) -> int:
        angle = gyro.get_theta()['z']
        return angle
    
    def spinToAngle(self, setPoint: int) -> None:
        error: float = setPoint - GyroMovement.getYaw(self._gyro)

        while (abs(error) > self._errorOffset):
            speed: float = self._pidYaw.pidCalc(error)

            if (speed > 10 and speed < 30):
                speed += 20
            
            if (speed < -10 and speed > -30):
                speed -= 20

            speeds: list[int] = motor7046.calculate_rotation_speed(speed)
            self.motors.setSpeed(speeds[0], speeds[1], speeds[2], speeds[3])

            sleep(0.3)
            error: float = setPoint - GyroMovement.getYaw(self._gyro)

if __name__ == "__main__":
    mov = GyroMovement(1)
    mov.spinToAngle(90)
