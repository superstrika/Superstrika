#!/usr/bin/env python3
import smbus
import time

# For the Raspberry Pi 4, the correct I2C bus is typically 1
BUS_NUMBER = 1  
bus = smbus.SMBus(BUS_NUMBER)

print(f"Scanning I2C bus {BUS_NUMBER} for devices...")
found_devices = []

# I2C addresses range from 0x03 to 0x77
for device in range(0, 120):
    print(f"Trying {device}")
    try:
        # Try reading a single byte from the device address
        bus.read_byte(device)
        found_devices.append(hex(device))
        print(f"yay at {device}")
    except IOError:
        # An IOError means no device responded at that address
        pass

if found_devices:
    print(f"Found {len(found_devices)} I2C device(s) at addresses: {', '.join(found_devices)}")
else:
    print("No I2C devices found.")
