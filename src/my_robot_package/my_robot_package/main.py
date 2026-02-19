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

logging.basicConfig(filename=data.LOG_PATH, filemode='w', level=logging.DEBUG, format=data.LOG_FORMAT)

class Hunt:
    def __init__(self):
        # motors
        self.servo = servo.Servo(data.SERVO_PIN, data.CHIP_ID)
        self.motors = motor.multipleMotors(data.MOTOR_PINS, data.CHIP_ID)

        #sensors
        self.gyro = gyro.MPU6050(data.I2C_ID)
        self.serial = serial7046.Serial7046(data.SERIAL_FREQUENCY)

        # processes
        self.lineDetection = edgeLineDetection.EdgeLineDetection(data.TCRT_PINS, data.CHIP_ID)

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

        for angle in range(data.MAX_ANGLE, data.MIN_ANGLE, -10):

            self.servo.angle = angle
            sleep(delay) # seconds

            ballX, ballY = self.serial.getBallLocation()
            if ballX != 0 or ballY != 0:
                self.log.info(f"Ball Found: {ballX}, {ballY}")
                print(f"Ball Found: {ballX}, {ballY}")
                return ballX, ballY


        self.log.info("Camera Search failed...")
        print("Camera Search failed...")
        return None

    def spinSearch(self, delay=0.3) -> tuple[float, float] | None:
        """
        Spins the robot 360 degrees or until ball is found.
        :param delay: the delay between the start of spinning to first angle check.
        :return: [0] - X coordinate of the returned object. [1] - Y coordinate of the returned object. None if not found.
        """

        self.log.info("Initializing Spin Search...")
        print("Initializing Spin Search...")

        startAngle = self.gyro.get_z_angle()

        self.motors.setSpeed(*tuple(motor.motor7046.calculate_rotation_speed(data.ROTATION_SPEED)))
        sleep(delay)
        print(f"DEBUG: {self.gyro.get_z_angle()} <- {startAngle}")

        angle = self.gyro.get_z_angle()
        while (startAngle + data.SPIN_SEARCH_ERROR < angle) and (startAngle - data.SPIN_SEARCH_ERROR > angle):

            ballX, ballY = self.serial.getBallLocation()
            if ballX != 0 or ballY != 0:
                self.motors.setSpeedVxVy(0, 0)
                self.log.info(f"Ball Found: {ballX}, {ballY}")
                print(f"Ball Found: {ballX}, {ballY}")
                return ballX, ballY

            angle = self.gyro.get_z_angle()
            print(f"Angle: {angle}")

        self.log.info("Spin search failed...")
        print("Spin search failed...")

    def spinToBall(self) -> None:
        """
        Spins the robot until robot is straight at the ball.
        """

        self.log.info("Spinning to Ball...")
        print("Spinning to Ball...")

        pid = PidCalc(0, 0, 0, 100, 100, 500, verbose=False)

        error = self.serial.getBallLocation()[0]
        while abs(error) > data.SPIN_TO_BALL_ERROR:
            speed = pid.pidCalc(error)

            speeds = motor.motor7046.calculate_rotation_speed(speed)

            self.motors.setSpeed(*tuple(speeds))
            error = self.serial.getBallLocation()[0]

        self.log.info("Spun successfully...")
        print("Spun successfully...")

    def goToBall(self, delay=0.3) -> None:
        self.log.info("Going to Ball...")
        print("Going to Ball...")
        sp = data.ROBOT_BALL_DISTANCE

        pid = PidCalc(0, 0, 0, 100, 100, 500, verbose=False)
        pv = self.serial.getBallLocation()[1] # Y distance

        while abs(pv - sp) > data.GO_TO_BALL_ERROR:
            speed = pid.pidCalc(pv - sp)
            self.motors.setSpeed(*tuple(motor.motor7046.calculate_speed(0, speed, 0)))

            sleep(delay)
            pv = self.serial.getBallLocation()[1]

        self.log.info(f"Got to Ball successfully... e: {pv - sp}")
        print(f"Got to Ball successfully... e: {pv - sp}")

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

