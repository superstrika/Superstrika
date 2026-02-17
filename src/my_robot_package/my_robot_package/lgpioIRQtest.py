import lgpio
from time import sleep

rising: bool = False
pin = 4

h = lgpio.gpiochip_open(0)
lgpio.RISING_EDGE if rising else lgpio.FALLING_EDGE

_last_interrupt_time = 0
_debounce_time = 100000  # In micro seconds.

def escape_func():
    print("Yayyy!")

def callback(chip, pin, level, system_tick):
        global _last_interrupt_time
        # 'level' will be 0 (falling/detected) or 1 (rising/cleared)
        print(f"Hardware Edge Detected! Level: {level}")
        
        # Match your desired edge
        target = 0 if state == lgpio.FALLING_EDGE else 1
        
        if level == target:
            dt = system_tick - _last_interrupt_time
            if dt > _debounce_time:
                escape_func()
                _last_interrupt_time = system_tick


lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_UP)
cb = lgpio.callback(h, pin, lgpio.BOTH_EDGES, callback)
print(f"Monitoring BCM Pin {pin}...")

while True:
    sleep(0.1)