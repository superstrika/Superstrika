from gpiozero import PWMLED
from time import sleep

# Pin 19 (BCM numbering)
led = PWMLED(22)

print("Running PWM test on GPIO19... Press CTRL+C to stop.")

try:
    while True:
        # 
        led.value = 1   



except KeyboardInterrupt:
    print("\nExiting program.")
    led.off()
