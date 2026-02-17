import serial
from pidCalc import PidCalc
import os
import motor

class CamMovement():

    def __init__(self) -> None:

        self.pidX = PidCalc(1, 0.0, 0.01, 10, 100, 50, "camPidX", False)
        self.pidY = PidCalc(1, 0.0, 0.01, 10, 100, 50, "camPidY", False)
        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=2
        )

        self.motors = motor.multipleMotors([19, 20, 21, 22, 23, 24, 25, 6])

    def scanForMessages(self) -> None:
        avg = []
        while True:
            # print(self.ser.in_waiting)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').rstrip()
                # print("Received:", response)

                try:
                    response: list[float] = response.split('#')
                    for i in range(len(response)):
                        response[i] = float(response[i])

                    # print(response)
                    avg.append((response[0], response[1]))

                    if (len(avg) == 5):
                        avgX = 0
                        avgY = 0
                        for r in avg:
                            avgX += r[0]
                            avgY += r[1]
                        avgX /= len(avg)
                        avgY /= len(avg)

                        Vx = self.pidX.pidCalc(avgX)
                        Vy = self.pidY.pidCalc(avgY)

                        speeds = motor.motor7046.calculate_speed(Vx, Vy, 0)
                        print(speeds)
                        self.motors.setSpeed(speeds[1], speeds[0], speeds[3], speeds[2])

                        # os.system('cls' if os.name == 'nt' else 'clear')
                        # print("----------------------------------------")
                        # print(f"Vx: {Vx}")
                        # print(f"Vy: {Vy}")
                        avg.clear()

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
    rob = CamMovement()
    rob.scanForMessages()

if __name__ == "__main__":
    main()
    
    