import gpiodIRQ

class Switch7046:
    def __init__(self, parent, button_pin: int):
        self.parent = parent
        self.sensor = gpiodIRQ.GPIOD_IRQ(pin=button_pin, escape_func=self.toggle_pause, rising=False)

        print("Switch is Ready!")
    
    def toggle_pause(self):
        if self.parent.running_gate.is_set():
            print("[!] PAUSEING")
            self.parent.running_gate.clear()
            self.parent.motors.setSpeed(0, 0, 0, 0)

        else:
            print("\n[>] RESUMING")
            self.parent.running_gate.set()
        