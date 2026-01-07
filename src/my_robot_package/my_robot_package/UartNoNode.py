import serial
from pidCalc import PidCalc

class UartNode():

    def __init__(self) -> None:

        self.pidX = PidCalc(1, 1, 1, 100, 50)
        self.pidY = PidCalc(1, 1, 1, 100, 50)
        
        self.ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            timeout=1
        )

    def scanForMessages(self) -> None:
        while True:
            print(self.ser.in_waiting)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').rstrip()
                print("Received:", response)

                try:
                    response: list[float] = response.split('#')
                    for i in range(len(response)):
                        response[i] = float(response[i])

                    print(response)

                except Exception as e:
                    print(e)
            # else:
                # print("Still Waiting...")

    def distanceToVelocity(self, msg: list) -> None:

        speed:list = [
            self.pidX.pidCalc(msg[0]),
            self.pidY.pidCalc(msg[1])
        ]
        #for now, no use of goals

        print(f"Vx: {speed[0]}, Vy: {speed[1]}")
def main() -> None:
    uart = UartNode()
    uart.scanForMessages()

if __name__ == "__main__":
    main()
    
    