import board
import busio
import adafruit_vcnl4040

class VCNL4040Wrapper:
    def __init__(self, i2c_bus=None):
        """
        Initialize the sensor.
        :param i2c_bus: Optional. Pass an existing I2C bus object. 
                        If None, it creates a new connection using board.I2C().
        """
        try:
            # 1. Setup I2C (Create it if not provided)
            if i2c_bus is None:
                self.i2c = board.I2C()  # uses board.SCL and board.SDA
            else:
                self.i2c = i2c_bus

            # 2. Initialize the Driverp
            self.sensor = adafruit_vcnl4040.VCNL4040(self.i2c)
            
            # 3. Configure for Maximum Range (200mA)
            # This makes the sensor 'see' further by default
            self.sensor.proximity_led_current = adafruit_vcnl4040.LED_200MA
            
            print("VCNL4040 Initialized successfully.")
            self.connected = True

        except ValueError:
            print("ERROR: VCNL4040 not found at address 0x60. Check wiring!")
            self.connected = False
        except Exception as e:
            print(f"ERROR: An unexpected error occurred: {e}")
            self.connected = False

    def get_proximity(self):
        if not self.connected: return 0
        try:
            return self.sensor.proximity
        except OSError:
            return 0

    def get_lux(self):
        """Returns ambient light in Lux. Returns 0.0 if error."""
        if not self.connected: return 0.0
        try:
            return self.sensor.lux
        except OSError:
            return 0.0

    def is_object_detected(self, threshold=65000):
        """
        Returns True if an object is closer than the threshold.
        :param threshold: The sensitivity value 
        """
        return self.get_proximity() > threshold

    def get_data(self):
        return {
            "proximity": self.get_proximity(),
            "lux": self.get_lux(),
            "object_detected": self.is_object_detected()
        }