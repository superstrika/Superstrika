"""----------------------------------------------
                   GPIO
----------------------------------------------"""
# MOTOR_PINS: list[int] = [25, 26, 21, 22, 23, 24, 19, 20]
# MOTOR_PINS: list[int] = [19, 20, 23, 24, 25, 26, 21, 22]
MOTOR_PINS: list[int] = [23, 24, 21, 22, 25, 26, 19, 20]
TCRT_PINS: list[int] = [1, 0, 5]
SERVO_PIN: int = 6
RELAY_PIN: int = 7

DRIBLER_PIN: list[int] = [13, 16]

"""----------------------------------------------
              Chip configuration
----------------------------------------------"""
I2C_ID: int = 1
CHIP_ID: int = 0

"""----------------------------------------------
              Camera configuration
----------------------------------------------"""
MIN_ANGLE: int = 75
MAX_ANGLE: int = 180

"""----------------------------------------------
              Serial configuration
----------------------------------------------"""
SERIAL_FREQUENCY: int = 115200

"""----------------------------------------------
               Log configuration
----------------------------------------------"""
LOG_PATH: str = './logs/main.log'
LOG_FORMAT: str = "[%(levelname)s] %(cls)s: %(funcName)s: %(message)s"

"""----------------------------------------------
              Hunt Configuration
----------------------------------------------"""
ROTATION_SPEED: int = 25

SPIN_SEARCH_ERROR: float = 3
SPIN_TO_BALL_ERROR: float = 1.5
GO_TO_BALL_ERROR: float = 1
ROBOT_BALL_DISTANCE: float = (1, 1)

"""----------------------------------------------
              Game configuration
----------------------------------------------"""
SELF_IS_BLUE: bool = True