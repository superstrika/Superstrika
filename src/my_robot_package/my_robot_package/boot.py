import lgpio
import time

h = lgpio.gpiochip_open(0)

pins = [i for i in range(19, 27)]

for pin in pins:
    try:
        lgpio.gpio_claim_output(h, pin)
        lgpio.tx_pwm(h, pin, 800, 0)
        print(f"Hardware updated: GPIO {pin} is now at {0}%")

    except Exception as e:
        print(f"Error: {e}")


time.sleep(0.1)