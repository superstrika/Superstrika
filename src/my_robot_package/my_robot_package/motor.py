from gpiozero import PWMLED
print(0)
class Motor:
    def __init__(self, pin1, pin2):
        # PWMLED allows for variable brightness/speed control
        self.in1 = PWMLED(pin1)
        self.in2 = PWMLED(pin2)

    def forward(self, speed=1.0):
        self.in1.value = speed  # Set speed (0.0 to 1.0)
        self.in2.value = 0      # Ensure other pin is off

    def backward(self, speed=1.0):
        self.in1.value = 0
        self.in2.value = speed

    def stop(self):
        self.in1.value = 0
        self.in2.value = 0



from time import sleep

# Initialize motor on GPIO pins 17 and 18
motor = Motor(23, 24)
print(1)

print("Moving forward at 50% speed...")
motor.forward(speed=0.5)
sleep(5)

print("Moving backward at full speed...")
motor.backward(speed=1.0)
sleep(2)

print("Stopping...")
motor.stop()
