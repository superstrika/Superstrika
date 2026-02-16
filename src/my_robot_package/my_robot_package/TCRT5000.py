import lgpio
import input7046
from time import sleep

class TCRT5000:
    
    def __init__(self, pin, chipID=0):
        self._sensor = input7046.Input7046(pin, chipID=chipID)
        self._Field_value: int = None
        self._value = None


    def calibrate(self, duration=1):
        print("Calibrating TCRT5000...")
        reading = []

        for _ in range(duration * 100):
            reading.append(self._sensor.read())
            sleep(0.01)

        self._Field_value = 0 if reading.count(0) > reading.count(1) else 1
        print(f"Calibration completed! Filed_value set to: {self._Field_value}")


    def read(self):
        digital_read = self._sensor.read() 
        self._value = 0 if digital_read == self._Field_value else 1

        return self._value
    
    @property
    def value(self):
        return self.read()

if __name__ == "__main__":
    s = TCRT5000(4)
    s.calibrate()

    while True:
        print(s.value)
