from gpiozero import PWMOutputDevice
from time import sleep
pins = [19, 20, 21, 22, 23, 24, 25, 26]

devices = [PWMOutputDevice(pin) for pin in pins]

for device in devices:
    device.value = 0  # sets output to 0
sleep(2)