from gpiozero import Motor
from time import sleep

# Create motor object
motor = Motor(forward=23, backward=24)

try:
    while True:
        print("Motor: forward")
        motor.forward()
        sleep(2)

        print("Motor: backward")
        motor.backward()
        sleep(2)

        print("Motor: stop")
        motor.stop()
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
    motor.stop()
