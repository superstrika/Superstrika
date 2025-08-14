from smbus2 import SMBus as I2C
from Gyro import MPU6050  
import time

i2c = I2C(1)

try:
    gyro = MPU6050(i2c, addr=0x68)
    print("MPU6050 initialized successfully!")
except RuntimeError as e:
    print(f"Failed to initialize MPU6050: {e}")
    exit(1)
    

i = 100

print("Reading angles (first set)...")
for _ in range(i):
    angle = gyro.get_theta()
    print(f" X={angle['x']}, Y={angle['y']}, Z={angle['z']}")
    time.sleep(0.2)

gyro.reset_theta()
print("\nTheta reset.\n")

print("Reading angles (second set after reset)...")
for _ in range(i):
    angle = gyro.get_theta()
    print(f"Angle: X={angle['x']}, Y={angle['y']}, Z={angle['z']}")
    time.sleep(0.2)

# Clean up
i2c.close()
