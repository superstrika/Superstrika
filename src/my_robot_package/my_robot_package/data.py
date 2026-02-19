"""----------------------------------------------
                   GPIO
----------------------------------------------"""
MOTOR_PINS: list[int] = [19, 20, 21, 22, 23, 24, 25, 8]
TCRT_PINS: list[int] = [4, 5, 0]
SERVO_PIN: int = 6
RELAY_PIN: int = 7

DISABLED_MOTOR_PIN: int = 26 # Grounded by mistake. Fix: changed 26 to 8.

"""----------------------------------------------
              Chip configuration
----------------------------------------------"""
I2C_ID: int = 1
CHIP_ID: int = 0

"""----------------------------------------------
              Camera configuration
----------------------------------------------"""
MIN_ANGLE: int = 140
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
ROTATION_SPEED: int = 30

SPIN_SEARCH_ERROR: float = 3
SPIN_TO_BALL_ERROR: float = 1
GO_TO_BALL_ERROR: float = 1
ROBOT_BALL_DISTANCE: float = 1

"""----------------------------------------------
              Game configuration
----------------------------------------------"""
SELF_IS_BLUE: bool = True