import lgpio

class IRQ:
    def __init__(self, pins: list, escape_funcs: list, chipID=0):
        self._chipID = chipID
        self._h = lgpio.gpiochip_open(chipID)
        
        if len(pins) != 3 or len(escape_funcs) != 3:
            raise ValueError("Must provide exactly 3 pins and 3 escape functions")

        self._pins = pins
        self._escape_funcs = escape_funcs
        self._last_interrupt_time = [0, 0, 0]  

        self._debounce_time = 100000  # In micro seconds.

    def _callback(self, chip, pin, state, system_tick):
        if pin in self._pins:
            _ = self._pin[pin]
            
            if state == 1:
                dt = system_tick - self._last_interrupt_time[_]
                
                if dt > self._debounce_time:
                    self._escape_funcs[_]()
                    
                    self._last_interrupt_time[_] = system_tick

    def start(self):
        for pin in self._pins:
            lgpio.gpio_claim_input(self._h, pin) # Pin defined as an input.
        
            lgpio.gpio_claim_alert_event(self._h, pin, lgpio.RISING_EDGE) # Alert event for 0->1 (green to white)changes.
            
            lgpio.gpio_set_alert_func(self._h, pin, self._callback)
            
        print("Interrupt-based monitoring started.")

    def close(self):
        lgpio.gpiochip_close(self._h)