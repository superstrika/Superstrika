import servo
import motor
from time import sleep
import edgeLineDetection
import gyro
import input7046
import data
import logging
import serial7046
from pidCalc import PidCalc
import gyroMovement
import math

try:
    from machine import I2C
except ImportError:
    from smbus2 import SMBus as I2C  # For RPI compatibility

logging.basicConfig(filename=data.LOG_PATH, filemode='w', level=logging.DEBUG, format=data.LOG_FORMAT)

class Hunt:
    def __init__(self):
        # motors
        self.i2c = I2C(data.I2C_ID)
        self.servo = servo.Servo(data.SERVO_PIN, data.CHIP_ID)
        self.motors = motor.multipleMotors(data.MOTOR_PINS, data.CHIP_ID, verbose=False, speedVerbose=True)

        #sensors
        self.gyro = gyro.MPU6050(self.i2c)
        self.serial = serial7046.Serial7046(data.SERIAL_FREQUENCY)

        # processes
        self.lineDetection = edgeLineDetection.EdgeLineDetection(pins=data.TCRT_PINS, chipID=data.CHIP_ID, motors=self.motors)
        self.gyroMovement = gyroMovement.GyroMovement(self.i2c, self.gyro, self.motors, pidValues=[0.25, 0.01, 0.01, 500, 100, 100])

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def camSearch(self, delay=0.3) -> tuple[float, float] | None:
        """
        Changes camera angle until ball is found.
        :param delay: the delay each change of angle.
        :return: [0] - X coordinate of the returned object. [1] - Y coordinate of the returned object. None if not found.
        """

        self.log.info("Initializing Camera Search...")
        print("Initializing Camera Search...")

        self.servo.angle = data.MAX_ANGLE

        for angle in range(data.MAX_ANGLE, data.MIN_ANGLE, -10):

            self.servo.setAngle(angle, delay * ((data.MAX_ANGLE - angle) / data.MIN_ANGLE))

            ballX, ballY = self.serial.getBallLocation()
            if ballX != 0 or ballY != 0:
                self.log.info(f"Ball Found: {ballX}, {ballY}")
                print(f"Ball Found: {ballX}, {ballY}")
                return ballX, ballY


        self.log.info("Camera Search failed...")
        print("Camera Search failed...")
        return None

    def spinSearch(self, delay=0.25, right: bool = True) -> tuple[float, float] | None:
        """
        Spins the robot 360 degrees or until ball is found.
        :param delay: the delay between the start of spinning to first angle check.
        :param right: the direction of the spinning
        :return: [0] - X coordinate of the returned object. [1] - Y coordinate of the returned object. None if not found.
        """
        speed = data.ROTATION_SPEED if right else -data.ROTATION_SPEED

        self.log.info("Initializing Spin Search...")
        print("Initializing Spin Search...")

        startAngle = self.gyro.get_z_angle()
        speeds = motor.motor7046.calculate_rotation_speed(speed)
        self.motors.setSpeed(*tuple(speeds))
        sleep(delay)
        print(f"DEBUG: {self.gyro.get_z_angle()} <- {startAngle}")

        angle = self.gyro.get_z_angle()
        print(f"DEBUG: angle: {angle}")
        print(f"DEBUG: startAngle: {startAngle}")
        print(f"DEBUG: error: {data.SPIN_SEARCH_ERROR}")
        while (startAngle + data.SPIN_SEARCH_ERROR > angle) or (startAngle - data.SPIN_SEARCH_ERROR < angle):
            self.motors.setSpeedVxVy(0, 0)
            ballX, ballY = self.serial.getBallLocation()
            if ballX != 0 or ballY != 0:
                self.log.info(f"Ball Found: {ballX}, {ballY}")
                print(f"Ball Found: {ballX}, {ballY}")
                return ballX, ballY

            
            angle = self.gyro.get_z_angle()
            print(f"Angle: {angle}")
            self.motors.setSpeed(*tuple(speeds))
            sleep(delay)

        self.log.info("Spin search failed...")
        print("Spin search failed...")

    def spinToBall(self) -> None:
        """
        Spins the robot until robot is straight at the ball.
        """
    
        self.log.info("Spinning to Ball...")
        print("Spinning to Ball...")
    
        pid = PidCalc(1.2, 0.2, 0.1, 150, 100, 500, verbose=False)
    
        error = self.serial.getBallLocation()[0]
        while abs(error) > data.SPIN_TO_BALL_ERROR:
            speed = pid.pidCalc(error)
    
            speeds = motor.motor7046.calculate_rotation_speed(speed)
    
            self.motors.setSpeed(*tuple(speeds))
            error = self.serial.getBallLocation()[0]
    
        self.motors.setSpeedVxVy(0, 0)

        if (self.serial.getBallLocation()[0] == 0):
            self.log.info("Spun too much: ball lost")
            print("Spun too much: ball lost")
            input
            self.spinSearch(right=error < 0, delay=0.15)
            self.spinToBall()
            return

        angle = self.gyro.get_z_angle()
        
        # print(f"Right now at {angle} deg.")

        # if error < 0:
        #     angle += 2
        # else:
        #     angle -= 2

        # print(f"Spinning to {angle} deg.")
        
        # self.gyroMovement.spinToAngle(angle)


        self.log.info("Spun successfully...")
        print("Spun successfully...")

    # def spinToBall(self):
    #     """
    #     Spins the robot until robot is straight at the ball.
    #     """
    #     ballX, ballY = self.serial.getBallLocation()
    #     print(f"ballX: {ballX}, ballY: {ballY}")
    #     lastError: int = 0

    #     while abs(ballX) > data.SPIN_TO_BALL_ERROR:
    #         angle = int(math.degrees(math.atan2(ballY, ballX)))
    #         # print(angle)

    #         self.log.debug(f"Found ball in angle: {angle}. Spinning...")
    #         print(f"Found ball in angle: {angle}. Spinning...")

    #         self.gyroMovement.spinToAngle(int(angle))

    #         lastError = angle
    #         ballX, ballY = self.serial.getBallLocation()

    #     if self.serial.getBallLocation()[0] == 0:
    #         self.motors.setSpeedVxVy(0, 0)
    #         self.log.info("Spun too much: ball lost")
    #         print("Spun too much: ball lost")
    #         input()
    #         self.spinSearch(right=lastError < 0)
    #         self.spinToBall()

    def goToBallX(self, delay=0.3) -> None:
        self.log.info("Going to BallX...")
        print("Going to BallX...")
        sp = data.ROBOT_BALL_DISTANCE

        pid = PidCalc(0.8, 0.1, 0.05, 100, 100, 500, verbose=False)
        pv = self.serial.getBallLocation()[1] # Y distance

        while abs(pv - sp) > data.GO_TO_BALL_ERROR:
            speed = pid.pidCalc(pv - sp)
            print(f"Speed {speed}")
            self.motors.setSpeed(*tuple(motor.motor7046.calculate_speed(0, speed, 0)))

            sleep(delay)
            pv = self.serial.getBallLocation()[1]

        self.log.info(f"Got to Ball successfully... e: {pv - sp}")
        print(f"Got to Ball successfully... e: {pv - sp}")
    
    def goToBall(self, delay=0.3) -> None:
        self.log.info("Going to BallX...")
        print("Going to BallX...")
        sp = data.ROBOT_BALL_DISTANCE

        pidY = PidCalc(0.5, 0.1, 0.1, 100, 100, 500, verbose=False)
        pidX = PidCalc(0.05, 0.05, 0.1, 100, 100, 500, verbose=False)
        pv = self.serial.getBallLocation() # distance

        while (abs(pv[0] - sp[0]) > data.GO_TO_BALL_ERROR) or (abs(pv[1] - sp[1]) > data.GO_TO_BALL_ERROR):
            speedX = pidX.pidCalc(pv[0] - sp[0])
            speedY = pidY.pidCalc(pv[1] - sp[1])
            print(f"Vx: {speedX}, Vy: {speedY}")
            self.motors.setSpeed(*tuple(motor.motor7046.calculate_speed(speedX, speedY, 0)))

            sleep(delay)
            pv = self.serial.getBallLocation()

        self.log.info(f"Got to Ball successfully... e: {pv[0] - sp[0]}, {pv[1] - sp[1]}")
        print(f"Got to Ball successfully... e: {pv[0] - sp[0]}, {pv[1] - sp[1]}")

    def hunt(self):
        ballX, ballY = self.camSearch()
        if ballX or ballY:
            # ball found
            pass
        else: #ball not found
            ballX, ballY = self.spinSearch()
            if ballX or ballY:
                #ball found
                pass
            else: # ball not found: returns to home.
                return # TODO

        # at this point, ballX + ballY is the ball coordinates

        self.spinToBall() # perfectly aligns with the ball

        # hit the ball:
        self.goToBall()

    def __del__(self):
        self.motors.setSpeedVxVy(0, 0)

if __name__ == "__main__":
    r = Hunt()
    # r.spinSearch(0.25)
    # r.spinToBall()
    # r.camSearch(delay=0.3)
    r.spinToBall()
    # while True:
    #     pass
    # r.spinSearch()
    # r.spinToBall()
    # r.goToBall()