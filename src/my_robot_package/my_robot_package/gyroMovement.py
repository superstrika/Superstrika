from pidCalc import PidCalc
from gyro import MPU6050
from motor import multipleMotors, motor7046
from smbus2 import SMBus as I2C  # For RPI compatibility
from time import sleep
import data
import motor
import time

class GyroMovement:
    
    def __init__(self, i2c: I2C = None, gyro: MPU6050 = None, motors: multipleMotors = None, pidValues: list[float] = [0.20, 0.1, 0.01, 10, 100, 100], errorOffset: float = 0.5):
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

            speeds: list[int] = motor7046.calculate_rotation_speed(-speed)
            self.motors.setSpeed(speeds[0], speeds[1], speeds[2], speeds[3])

            sleep(0.3)
            error: float = setPoint - self.gyro.get_z_angle()

    def move_forward_cm(self, distance_cm: float, speed=30):
        """
        Moves the robot forward for a specified distance with gyro heading correction.
        Note: This implementation uses time as a proxy for distance.
        For exact distance, motor encoders would be required.
        """
        # 1. Record the starting heading to maintain it
        target_heading = self.gyro.get_z_angle()
        pid = PidCalc(1.5, 0.01, 0.1, 100, 100, 500)

        # 2. Calculate duration based on distance (Calibration required)
        # Example: 0.05 seconds per cm at base speed 50
        duration = distance_cm * 0.05
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                # 3. Get current heading and calculate correction
                current_heading = self.gyro.get_z_angle()
                correction = pid.pidCalc(target_heading - current_heading)

                # 4. Apply correction to motor speeds
                # move_speed is forward (Y), correction is rotation (W)
                # calculate_speed(x, y, w)
                motor_speeds = motor.motor7046.calculate_speed(0, speed, correction)

                # 5. Set the calculated speeds
                self.motors.setSpeed(*motor_speeds)

                # Small sleep to prevent CPU hogging
                time.sleep(0.01)

        finally:
            # Always stop motors when done or if interrupted
            self.motors.stop()

if __name__ == "__main__":
    import dribbler

    # d = dribbler.Dribbler(data.DRIBLER_PIN)
    mov = GyroMovement()

    # d.start()
    # mov.move_forward_cm(15, 30)
    mov.spinToAngle(90)

    input()
    # d.stop()
