import gpiozero
import logging
from time import sleep
import time
from robot.consts.data import KICKER_PIN

class Kicker:
    CHARGING_TIME_SEC = 20
    KICKING_TIME_SEC = 0.5

    def __init__(self, pin1: int):
        self._lastInitializationTime = time.time()

        self._kicker = gpiozero.DigitalOutputDevice(pin1)

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def kick(self) -> bool:
        if (time.time() - self._lastInitializationTime) < self.CHARGING_TIME_SEC:
            return False

        self._kicker.on()
        sleep(self.KICKING_TIME_SEC)
        self._kicker.off()

        self._lastInitializationTime = time.time()
        return True

if __name__ == "__main__":
    input("Press Enter to kick")
    Kicker = Kicker(KICKER_PIN)
    Kicker.kick()