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

    def spinToBall(self) -> None:
        self.log.info("Spinning to Ball...")
        print("Spinning to Ball...")

        pid = PidCalc(0, 0, 0, 100, 100, 500, verbose=False)

        error = self.serial.getBallLocation()[0]
        while abs(error) > data.SPIN_MAX_ERROR:
            speed = pid.pidCalc(error)

            speeds = motor.motor7046.calculate_rotation_speed(speed)

            self.motors.setSpeed(*tuple(speeds))
            error = self.serial.getBallLocation()[0]

        self.log.info("Spun successfully...")
        print("Spun successfully...")