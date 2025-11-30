import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from pidCalc import PidCalc

class UartNode(Node):

    def __init__(self) -> None:
        super().__init__("uart")

        self.pidX = PidCalc(1, 1, 1, 100, 50)
        self.pidY = PidCalc(1, 1, 1, 100, 50)

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

                try:
                    response: list[float] = response.split('#')
                    for i in range(len(response)):
                        response[i] = float(response[i])

                    xy = Float32MultiArray()
                    xy.data = response
                    self.xyPublisher.publish(xy)

                except Exception as e:
                    print(e)

    def distanceToVelocity(self, msg: Float32MultiArray) -> None:
        speed = Float32MultiArray()

        speed.data = [
            self.pidX.pidCalc(msg.data[0]),
            self.pidY.pidCalc(msg.data[1])
        ]
        #for now, no use of goals

        self.VxVyPublisher.publish(speed)

def main() -> None:
    uart = UartNode()
    uart.scanForMessages()

if __name__ == "__main__":
    main()
    
    