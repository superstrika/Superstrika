import serial
import os
import logging

class Serial7046:
    def __init__(self, freq=115200):
        self.ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=freq,
            timeout=2
        )

        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {'cls': self.__class__.__name__}
        )

    def readMessage(self):
        while True:
            if self.ser.in_waiting > 0:
                return self.ser.readline().decode('utf-8').rstrip()

    def getBallLocation(self) -> tuple[float, float] | None:
        ballLocation: list[tuple[float, float]] = []
        try:
            for _ in range(5):
                response = self.readMessage()
                print(response)

                response: list[float] = response.split('#')
                for i in range(len(response)):
                    response[i] = float(response[i])

                ballLocation.append((response[0], response[1]))

            avgX: float = 0
            avgY: float = 0
            for r in ballLocation:
                avgX += r[0]
                avgY += r[1]
            avgX /= len(ballLocation)
            avgY /= len(ballLocation)

            return avgX, avgY

        except Exception as e:
            self.log.error(e)
            print(e)

    def getBlueGoalLocation(self) -> tuple[float, float] | None:
        goalLocation: list[tuple[float, float]] = []
        try:
            for _ in range(5):
                response = self.readMessage()

                response: list[float] = response.split('#')
                for i in range(len(response)):
                    response[i] = float(response[i])

                goalLocation.append((response[2], response[3]))

            avgX: float = 0
            avgY: float = 0
            for r in goalLocation:
                avgX += r[0]
                avgY += r[1]
            avgX /= len(goalLocation)
            avgY /= len(goalLocation)

            return avgX, avgY

        except Exception as e:
            self.log.error(e)
            print(e)

    def getYellowGoalLocation(self) -> tuple[float, float] | None:
        goalLocation: list[tuple[float, float]] = []
        try:
            for _ in range(5):
                response = self.readMessage()

                response: list[float] = response.split('#')
                for i in range(len(response)):
                    response[i] = float(response[i])

                goalLocation.append((response[4], response[5]))

            avgX: float = 0
            avgY: float = 0
            for r in goalLocation:
                avgX += r[0]
                avgY += r[1]
            avgX /= len(goalLocation)
            avgY /= len(goalLocation)

            return avgX, avgY

        except Exception as e:
            self.log.error(e)
            print(e)

    def getGoalLocation(self, blueGoal: bool) -> tuple[float, float] | None:
        if blueGoal:
            return self.getBlueGoalLocation()
        return self.getYellowGoalLocation()