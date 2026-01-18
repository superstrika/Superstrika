import lgpio
from time import sleep

# UART Pins (BCM numbering)
TX_PIN = 14
RX_PIN = 15

# Open the GPIO chip (0 is the default for Pi 4)
handle = lgpio.gpiochip_open(0)

def check_pins():
    print(f"{'GPIO':<10} | {'LEVEL':<10}")
    print("-" * 22)
    
    for pin in [TX_PIN, RX_PIN]:
        # Get the logical level (0 or 1)
        # Note: lgpio_gpio_read works even if the pin is set to UART mode
        level = lgpio.gpio_read(handle, pin)
        
        state = "HIGH (3.3V)" if level == 1 else "LOW (0V)"
        print(f"GPIO {pin:<5} | {state}")

try:
    # lgpio.gpio_write(handle, TX_PIN, 0)
    # lgpio.gpio_write(handle, RX_PIN, 0)
    while True:
        check_pins()
        sleep(0.3)

finally:
    # Always close the handle to release resources
    lgpio.gpiochip_close(handle)