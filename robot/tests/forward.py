import sys

#from flask import logging

from robot.processes.MultipleMotors import MultipleMotors
import robot.consts.data as data


def main():
    motors = MultipleMotors(data.MOTOR_PINS)

    motors.setSpeed(0, 100, 0)
    input()
    motors.stop()

if __name__ == "__main__":
    main()
