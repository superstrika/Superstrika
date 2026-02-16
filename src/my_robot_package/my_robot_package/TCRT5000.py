import lgpio
import input7046
from time import sleep
import threading

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

class multipleTCRT5000:
    def __init__(self, pins: list[int], chipID=0):
        self.sensors = [TCRT5000(pin, chipID) for pin in pins]

    def calibrate(self, duration=1):
        threads = []
        for i in range(len(self.sensors)):
            threads.append(threading.Thread(target=self.sensors[i].calibrate))

            threads[i].start()

        for thread in threads:
            thread.join()

    @property
    def values(self):
        return [sensor.value for sensor in self.sensors]

def single_TCRT5000_test(pin: int, chipID=0):
    sensor = TCRT5000(pin, chipID)
    sensor.calibrate()

    while True:
        print(sensor.value)

def multiple_TCRT5000_test(pins: list[int], chipID=0):
    sensors = multipleTCRT5000(pins, chipID)
    sensors.calibrate()

    while True:
        print(sensors.values)

if __name__ == "__main__":
    multiple_TCRT5000_test([4, 5, 1])