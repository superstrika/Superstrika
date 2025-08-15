from gpiozero import PWMLED
from time import sleep

# Connect your LED (or other PWM device) to GPIO pin 18
led = PWMLED(18)

try:
    while True:
        # Fade in
        for duty in range(0, 101):
            led.value = duty / 100
            print(duty / 100)
            sleep(0.02)

        # Fade out
        for duty in range(100, -1, -1):
            led.value = duty / 100
            print(duty / 100)

            sleep(0.02)

except KeyboardInterrupt:
    led.off()
