import robot.components.motor as motor
from robot.consts.data import MOTOR_PINS

def main():
    # motor1 = motor.motor7046(MOTOR_PINS[0], MOTOR_PINS[1], switch=False) #FR
    # motor2 = motor.motor7046(MOTOR_PINS[2], MOTOR_PINS[3], switch=True) #FL
    motor3 = motor.motor7046(MOTOR_PINS[4], MOTOR_PINS[5], switch=True) #BL
    motor4 = motor.motor7046(MOTOR_PINS[6], MOTOR_PINS[7], switch=False) #BR

    motors = [motor3, motor4]

    for mot in motors:
        mot.speed = 100
    input()

if __name__ == "__main__":
    main()
