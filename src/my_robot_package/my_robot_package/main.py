import servo
import motor
from time import sleep
import edgeLineDetection
import gyro
import input7046
import data
import logging

logging.basicConfig(filename=data.LOG_PATH, filemode='w', level=logging.DEBUG, format=data.LOG_FORMAT)

class Hunt:
    def __init__(self):
        self.servo = servo.Servo(data.SERVO_PIN, data.CHIP_ID)
        self.motors = motor.multipleMotors(data.MOTOR_PINS, data.CHIP_ID)
        self.lineDetection = edgeLineDetection.EdgeLineDetection(data.TCRT_PINS, data.CHIP_ID)

        self.gyro = gyro.MPU6050(data.I2C_ID)

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def camSearch(self, delay=0.3):
        self.log.info("Initializing Camera Search...")
        for angle in range(data.MIN_ANGLE, data.MAX_ANGLE, 10):
            pass