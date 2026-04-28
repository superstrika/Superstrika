from motor import motor7046, multipleMotors
import data

def main() -> None:
    motors = multipleMotors(data.MOTOR_PINS)
    speed = 100
    speeds = tuple(motor7046.calculate_speed(-100, 0, 0))
    print(speeds)
    motors.setSpeed(*speeds)
    # motors.setSpeed(50, 50, -50, -50)
    input()
    # motors.setSpeed(0, 0, 0, 0)

    


if __name__ == "__main__":
    main()