from gpiozero import AngularServo
from time import sleep

# Initialize AngularServo on GPIO 17 with custom pulse widths for full 180° range
servo = AngularServo(
    6, min_angle=0, max_angle=180,
    min_pulse_width=0.0005, max_pulse_width=0.0024
)

try:
    servo.angle = 0
    input()
    servo.angle = 90
    input()
    servo.angle = 180
    input()
except KeyboardInterrupt:
    servo.detach()

