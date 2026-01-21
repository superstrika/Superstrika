import serial
from pidCalc import PidCalc

class UartNode():

    def __init__(self) -> None:

        self.pidX = PidCalc(1, 1, 1, 100, 50)
        self.pidY = PidCalc(1, 1, 1, 100, 50)
        
        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=2
        )

    def scanForMessages(self) -> None:
        while True:
            # print(self.ser.in_waiting)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                print("Received:", response)

                try:
                    response: list[str] = response.split('#')
                    for i in range(len(response)):
                        if response[i][:2] == "0-":
                            response[i].removeprefix("0-")
                        response[i] = float(response[i])

                    print(response)
                    self.distanceToVelocity(response)
                    

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
    
    