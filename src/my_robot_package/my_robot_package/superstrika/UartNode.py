import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class UartNode(Node):

    def __init__(self) -> None:
        super().__init__("uart")

        self.xyPublisher = self.create_publisher(
            Float32MultiArray,
            'xy',
            10
        )

        self.xyListener = self.create_subscription(
            Float32MultiArray,
            'xy',
            self.distanceToVelocity,
            10
        )

        self.VxVyPublisher = self.create_publisher(
            Float32MultiArray,
            'VxVy',
            11
        )

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

    def distanceToVelocity(self, msg: Float32MultiArray) -> None:
        pass


def main() -> None:
    uart = Uart()
    uart.scanForMessages()

if __name__ == "__main__":
    main()
    
    