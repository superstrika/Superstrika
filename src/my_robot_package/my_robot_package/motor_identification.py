from motor import multipleMotors, motor7046
import data

def main() -> None:
    motors = multipleMotors(data.MOTOR_PINS)
    speed = -100

    print(speed)
    motors.setSpeed(speed, 0, 0, 0)
    input()
    motors.setSpeed(0, speed, 0, 0)
    input()
    motors.setSpeed(0, 0, speed, 0)
    input()
    motors.setSpeed(0, 0, 0, speed)
    input()


if __name__ == "__main__":
    main()