import lgpio
from TCRT5000 import TCRT5000
import threading
from time import sleep


class IRQ:
    def __init__(self, pins: list, escape_funcs: list, chipID=0):
        self._chipID = chipID
        
        if len(pins) != 3 or len(escape_funcs) != 3:
            raise ValueError("Must provide exactly 3 pins and 3 escape functions")

        self._sensors = [TCRT5000(pin, chipID) for pin in pins]
        self._escape_funcs = escape_funcs
        
        self._running = False
        self._thread = None
        

    def _monitor_sensors(self):
        while self._running:
            for _ in range(3):
                if self._sensors[_].read() == 1:
                    print(f"Sensor {_} triggered!")
                    self._escape_funcs[_]()
                    
            sleep(0.01)  

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._monitor_sensors)
            self._thread.start()
            print("IRQ monitoring started.")

    def stop(self):
        if self._running == True:
            self._running = False
            self._thread.join()
            print("IRQ monitoring stopped.")
                    