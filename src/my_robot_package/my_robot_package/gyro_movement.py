from pidCalc import PidCalc
from gyro import MPU6050
from motor import multipleMotors, motor7046
from smbus2 import SMBus as I2C  # For RPI compatibility
from time import sleep

class GyroMovemnet:
    
    def __init__(self, errorOffset: float = 0.5):
        self._i2c = I2C(1)
        self._gyro = MPU6050(self._i2c)

        self.motors = multipleMotors([19, 20, 21, 22, 23, 24, 25, 6])
        self._pidYaw = PidCalc(0.05, 0.01, 0.1, 100, 100)
        self._errorOffset = errorOffset

    @staticmethod
    def getYaw(gyro: MPU6050) -> int:
        angle = gyro.get_theta()['z']
        return angle
    
    def move(self, setPoint: int) -> None:
        error: float = setPoint - GyroMovemnet.getYaw(self._gyro)
        while (abs(error) > self._errorOffset):
            error: float = setPoint - GyroMovemnet.getYaw(self._gyro)
            speed: float = self._pidYaw.pidCalc(error)
            print(speed)
            speeds: list[int] = motor7046.calculate_speed(speed, -speed, 0)
            x = speeds[0] if abs(speeds[0]) > abs(speeds[1]) else speeds[1]
            y = speeds[1] if abs(speeds[2]) > abs(speeds[3]) else speeds[3]
            self.motors[0].speed = x
            self.motors[1].speed = x
            self.motors[2].speed = y
            self.motors[3].speed = y
            # for i in range(2):
            #     print(int(speeds[i]), end=", ")
            #     speed = speeds[i]
                
            #     if (speed < 1 and speed > -1): speed = 0 
            #     self.motors[i].speed = speed
            #     self.motors[i+2].speed = speed

            print()
            sleep(0.3)

if __name__ == "__main__":
    mov = GyroMovemnet()
    mov.move(90)
