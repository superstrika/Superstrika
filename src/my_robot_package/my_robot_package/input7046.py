import lgpio

class Input7046:
    def __init__(self, pin: int, chipID=0):
        self._pin = pin

        self._h = lgpio.gpiochip_open(chipID)
        lgpio.gpio_claim_input(self._h, pin)

    def read(self):
        return lgpio.gpio_read(self._h, self._pin)
    
    @property
    def value(self):
        return self.read()
    
if __name__ == "__main__":
    pin: int = 4
    s = Input7046(pin)
    while True:
        print(s.value)
