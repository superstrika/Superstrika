from gpiozero import PWMOutputDevice
from time import sleep

class Motor:
    def __init__(self, pin1, pin2):
        # We use PWMOutputDevice for variable speed control
        self.in1 = PWMOutputDevice(pin1)
        self.in2 = PWMOutputDevice(pin2)

    def forward(self, speed=0.5):
        self.in1.value = speed  # Speed is 0.0 to 1.0
        self.in2.value = 0

    def backward(self, speed=0.5):
        self.in1.value = 0
        self.in2.value = speed

    def stop(self):
        self.in1.value = 0
        self.in2.value = 0

# Test with your specific pins
motor = Motor(25, 26)
print("Moving forward...")
motor.forward(0.5)
sleep(2)
motor.stop()
  