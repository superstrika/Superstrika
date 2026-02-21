##############################################
#                  Data
##############################################

MOTOR_PINS: list[int] = [19, 20, 21, 22, 23, 24, 25, 8]
TCRT_PINS: list[int] = [1, 0, 5]
SERVO_PIN: int = 6
RELAY_PIN: int = 7

DISABLED_MOTOR_PIN: int = 26 # Grounded by mistake. Fix: changed 26 to 8.

I2C_ID: int = 1
