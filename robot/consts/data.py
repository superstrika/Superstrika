"""----------------------------------------------
                   GPIO
----------------------------------------------"""

MOTOR_PINS: list[int] = [21, 22, 17, 18, 13, 16, 19, 20]
TCRT_PINS: list[int] = [1, 0, 5]
SERVO_PIN: int = 6
RELAY_PIN: int = 7

DRIBBLER_PIN: tuple[int, int] = (23, 24)
KICKER_PIN: int = 25
START_BUTTON_PIN: int = 4

"""----------------------------------------------
              Camera configuration
----------------------------------------------"""
MIN_ANGLE: int = 0
MID_ANGLE: int = 35
MAX_ANGLE: int = 70
# GOOD_ANGLE: int = 60

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
              Camera size configuration
----------------------------------------------"""

BALL_SIZE_CM: float = 4.3
GOAL_SIZE_CM: float = 64.0
CAMERA_HEIGHT_CM: float = 7.1

"""----------------------------------------------
              Hunt Configuration
----------------------------------------------"""
ROTATION_SPEED: int = 25

SPIN_SEARCH_ERROR: float = 3
SPIN_TO_BALL_ERROR: float = 1.5
GO_TO_BALL_ERROR: float = 1
GO_TO_BALL_MIN_SPEED: float = 40
# ROBOT_BALL_DISTANCE: tuple[float, float] = (0, 0)
ROBOT_GOAl_DISTANCE: int = 70

BALL_IN_KICKER_DISTANCE: int = 2 # cm
MOTOR_CROSS_ANGLE: int = 45

"""----------------------------------------------
              Game configuration
----------------------------------------------"""
SELF_IS_BLUE: bool = True

import socket

SELF_IS_HUNTER: bool = True if socket.gethostname() == "superstrika" else False
