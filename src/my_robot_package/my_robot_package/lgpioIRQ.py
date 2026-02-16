import lgpio

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

        self.start(pin)

        self.state = lgpio.RISING_EDGE if rising else lgpio.FALLING_EDGE

        self.escape_func = escape_func

    def start(self, pin: int):
        lgpio.gpio_claim_input(self._h, pin)
        lgpio.gpio_claim_alert_event(self._h, pin, self.state)  # Alert event for 0->1 (green to white)changes.
        lgpio.gpio_set_alert_func(self._h, pin, self.callback)

        print("Interrupt-based monitoring started.")

    def callback(self, chip, pin, state, system_tick):
        if state == self.state:
            dt = system_tick - self._last_interrupt_time

            if dt > self._debounce_time:
                self.escape_func()

                self._last_interrupt_time = system_tick

    def __del__(self):
        lgpio.gpiochip_close(self._h)

def escape():
    print("Interrupt triggered!")

if __name__ == "__main__":
    irq = IRQ7046(pin=4, escape_func=escape, rising=False)

    try:
        while True:
            pass  # Keep the main thread alive to listen for interrupts
    except KeyboardInterrupt:
        print("Exiting...")