from motor import multipleMotors, motor7046

def main() -> None:
    motors = multipleMotors([19, 20, 21, 22, 23, 24, 25, 6])
    speed = 100

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