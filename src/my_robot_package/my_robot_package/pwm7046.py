import lgpio
from time import sleep

class PWM7046:

    def __init__(self, pin, freq=800, chipID=0):

        self._pin = pin
        self._freq = freq
        self._value = 0

        self._h = lgpio.gpiochip_open(chipID)
        lgpio.gpio_claim_output(self._h, pin)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value_):
        if 0 <= value_ <= 100:
            self._value = value_

            lgpio.tx_pwm(self._h, self._pin, self._freq, self._value)
            print(f"Hardware updated: GPIO {self._pin} is now at {value_}%")

        else:
            raise Exception("Error: Value must be between 0 and 100!")
        
if __name__ == "__main__":
    # motors = [i for i in range(19, 27)]
    
    # for i in range(len(motors)):
    #     led = PWM7046(motors[i], 800)
    #     led2 = PWM7046(motors[i+1], 800)

    #     led.value = 20
    #     led.value = 0
    #     i += 1
    # mot1 = PWM7046(19)
    # mot2 = PWM7046(20)
    # mot3 = PWM7046(21)
    # mot4 = PWM7046(22)
    # mot5 = PWM7046(23)
    # mot6 = PWM7046(24)
    # mot7 = PWM7046(25)
    # mot8 = PWM7046(26)

    # value: int = 20
    # value2: int = 0
    # mot1.value = value
    # mot2.value = value2
    # mot3.value = value
    # mot4.value = value2
    # mot5.value = value
    # mot6.value = value2
    # mot7.value = value
    # mot8.value = value2

    

    led = PWM7046(12)
    # led2 = PWM7046(24, 800)
    led.value = 100
    # led2.value = 0

    input()
    # # for motor in motors:
    # #     led = PWM7046(motor, 800)

    #     led.value = 0
    # while True:
    #     led.value = 100
    #     print("ON")
    #     sleep(1)

    #     led.value = 0
    #     print("OFF")
    #     sleep(1)