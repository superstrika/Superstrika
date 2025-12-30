from gpiozero import PWMOutputDevice
from time import sleep
# pins = [19, 20, 21, 22, 23, 24, 25, 26]

# devices = [PWMOutputDevice(pin) for pin in pins]

# for device in devices:
#     device.value = 0.5  # sets output to 1    

# device = PWMOutputDevice(21)

# device.on()
# from gpiozero import LED
# from time import sleep

# led = LED(21)          # use BCM pin numbering
# led.on()               # set pin HIGH
# sleep(2)
# led.off()              # set pin LOW


# import RPi.GPIO as GPIO
# import time

# # Pin Configuration
# LED_PIN = 21  # Using Broadcom (BCM) numbering

# # Setup
# GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
# GPIO.setup(LED_PIN, GPIO.OUT) # Set pin to output mode

# print("Starting LED test. Press Ctrl+C to stop.")

# try:
#     for i in range(5):
#         print(f"Blink {i+1}: LED ON")
#         GPIO.output(LED_PIN, GPIO.HIGH) # Turn on (3.3V)
#         time.sleep(1)                   # Wait 1 second
        
#         print(f"Blink {i+1}: LED OFF")
#         GPIO.output(LED_PIN, GPIO.LOW)  # Turn off (0V)
#         time.sleep(1)                   # Wait 1 second

# except KeyboardInterrupt:
#     print("\nTest stopped by user")

# finally:
#     GPIO.cleanup() # Resets pins to safe state
#     print("GPIO cleaned up.")

import lgpio
import time

# GPIO 21 is Physical Pin 40
pins = [19, 20, 21, 22, 23, 24, 25, 26]
CHIP_ID = 0  # Confirmed by your gpiodetect

for pin in pins:
    try:
        # 1. Open the handle
        h = lgpio.gpiochip_open(CHIP_ID)
        
        # 2. CLAIM the pin as an output (This is the vital missing step)
        # This tells the kernel "I am using this pin now."
        lgpio.gpio_claim_output(h, pin)
        
        print(f"PWM Active on GPIO {pin}. LED should be at full brightness.")
        
        # 3. Start PWM (Frequency: 800Hz, Duty Cycle: 100%)
        lgpio.tx_pwm(h, pin, 800, 100)
        input()
        lgpio.tx_pwm(h, pin, 800, 0)


    except KeyboardInterrupt:
        print("\nUser stopped the test.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 4. Clean up: Stop PWM and release the chip handle
        if 'h' in locals():
            lgpio.tx_pwm(h, pin, 0, 0)
            lgpio.gpiochip_close(h)
        print("GPIO resources released.")