import smbus2 as smbus

bus = smbus.SMBus(20)  # instead of 1
print("Scanning I2C bus...")

for address in range(0x03, 0x78):
    try:
        bus.write_quick(address)
        print(f"Found device at 0x{address:02X}")
    except OSError:
        pass

print("Scan complete.")
