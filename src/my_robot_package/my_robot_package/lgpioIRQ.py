import lgpio
import TCRT5000
from time import sleep

class IRQ7046:
    def __init__(self, pin: int, escape_func, rising: bool, chipID=0):
        """
        Initializes the IRQ7046 class for
        monitoring a single GPIO pin with interrupt-based detection.
        :param pin: the GPIO pin to monitor
        :param escape_func: the function to call when the interrupt is triggered
        :param rising: True for rising edge (0->1), False for falling edge (1->0)
        :param chipID: chipID for the GPIO chip, default is 0
        """

        self._h = lgpio.gpiochip_open(chipID)

        self._last_interrupt_time = 0

        self._debounce_time = 100000  # In micro seconds.

        self.state = lgpio.RISING_EDGE if rising else lgpio.FALLING_EDGE

        self.escape_func = escape_func

        self.cb = None

        self.start(pin)

    # def start(self, pin: int):
    #     # lgpio.gpio_free(self._h, pin)
    #     lgpio.gpio_claim_input(self._h, pin, lgpio.SET_PULL_UP)
    #     self.cb = lgpio.callback(self._h, pin, self.state, self.callback)

    #     print(f"Interrupt-based monitoring started on pin {pin}")

    # def callback(self, chip, pin, state, system_tick):
    #     print("hi")
    #     state = lgpio.RISING_EDGE if state else lgpio.FALLING_EDGE
    #     if state == self.state:
    #         dt = system_tick - self._last_interrupt_time

    #         if dt > self._debounce_time:
    #             self.escape_func()

    #             self._last_interrupt_time = system_tick

    def start(self, pin: int):
        # Use PULL_UP because TCRT5000 usually pulls to Ground
        lgpio.gpio_claim_input(self._h, pin, lgpio.SET_PULL_UP)
        
        # Monitor BOTH edges for testing; if this doesn't print, it's a wiring/pin issue
        self.cb = lgpio.callback(self._h, pin, lgpio.BOTH_EDGES, self.callback)
        print(f"Monitoring BCM Pin {pin}...")

    def callback(self, chip, pin, level, system_tick):
        # 'level' will be 0 (falling/detected) or 1 (rising/cleared)
        print(f"Hardware Edge Detected! Level: {level}")
        
        # Match your desired edge
        target = 0 if self.state == lgpio.FALLING_EDGE else 1
        
        if level == target:
            dt = system_tick - self._last_interrupt_time
            if dt > self._debounce_time:
                self.escape_func()
                self._last_interrupt_time = system_tick

    def close(self):
        self.cb.cancel()
        lgpio.gpiochip_close(self._h)

def escape():
    print("Interrupt triggered!")

if __name__ == "__main__": 
    irq = IRQ7046(pin=4, escape_func=escape, rising=False)

    try:
        # sensors = TCRT5000.TCRT5000(4, 0)
        while True:
            # print(sensors.value)
            sleep(0.1)

    except KeyboardInterrupt:
        irq.close()
        print("Exiting...")