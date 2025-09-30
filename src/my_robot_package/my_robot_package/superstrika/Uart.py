import serial
import time

class Uart:

    def __init__(self) -> None:
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            timeout=1
        )

    def scanForMessages(self) -> None:
        while True:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').rstrip()
                print("Received:", response)


def main() -> None:
    uart = Uart()

    uart.scanForMessages()

if __name__ == "__main__":
    main()
    
    