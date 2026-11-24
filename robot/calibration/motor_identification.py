from robot.components.motor import motor7046
from robot.processes.MultipleMotors import MultipleMotors
import robot.consts.data as data
import gpiozero

def main() -> None:
    # relay = gpiozero.LED(8)
    # relay.on()
    motors = MultipleMotors(data.MOTOR_PINS)
    speed = 100

    #motors.setMotorOn(2, speed)

    #input()

    for i in range(4):
        motors.setMotorOn(i, speed)
        input("Press Enter to continue...")
        motors.setMotorOn(i, -speed)
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
