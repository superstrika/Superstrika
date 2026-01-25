from pwm7046 import PWM7046

class Relay:
    def __init__(self, signal_pin=7):
        self._pin = signal_pin
        self._relay = PWM7046(signal_pin, 800)
        self._state = False
        self.off()

    @property
    def state(self) -> bool:
        return self._state

    def on(self):
        self._relay.value = 100
        self._state = True
        print(f"Relay ON!")

    def off(self):
        self._relay.value = 0
        self._state = False
        print(f"Relay OFF!")


# if __name__ == "__main__":
#     relay = Relay(7)
#     relay.on()
#     input("Press Enter.")
#     relay.off()