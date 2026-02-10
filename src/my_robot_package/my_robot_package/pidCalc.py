import time
import os
import logging

class PidCalc:
    def __init__(self, kp: float, ki: float, kd: float, kt: float,  maxSpeed: float, maxIntegral: float, name: str = "pidCalc", verbose: bool = True) -> None:
        filename = f"log_{time.strftime('%H-%M-%S')}_{name}.txt"
        logging.basicConfig(filename=filename, filemode='w', level=logging.INFO, format='[%(levelname)s]: %(message)s')
        
        self.kp: float = kp
        self.ki: float = ki
        self.kd: float = kd
        self.kt: float = kt

        self.count = 0

        self.prevError: float = 0
        self.integral: float = 0

        self.lastTime: float = time.time()

        self.maxSpeed: float = abs(maxSpeed)
        self.maxIntegral: float = abs(maxIntegral)

        self.name = name
        self.verbose = verbose

    def pidCalc(self, error: float) -> float:
        if self.verbose:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"--------------------{self.name}--------------------------")
        logging.info(f"--------------------{self.name}--------------------------")
        self.count += 1
        dt = time.time() - self.lastTime


        self.integral += error * dt
        # self.integral = max(-self.maxIntegral, min(self.integral, self.maxIntegral))

        derivative = (error - self.prevError) / (self.kt * dt) if dt > 0.1 else 0.0
        if (self.count < 5):
            derivative = 0
        speed = self.kp * error + self.ki * self.integral + self.kd * derivative

        if self.verbose:
            print(f"Integral: {self.integral}")
            print(f"Derivative: {derivative}")
            print(f"Error: {error}")
            print(f"Speed: {speed}")
            print(f"Last Error: {self.prevError}")
            print(f"Dt: {dt}")

        logging.info(f"Integral: {self.integral}")
        logging.info(f"Derivative: {derivative}")
        logging.info(f"Error: {error}")
        logging.info(f"Speed: {speed}")
        logging.info(f"Last Error: {self.prevError}")
        logging.info(f"Dt: {dt}")

        self.lastTime = time.time()
        self.prevError = error

        # speed = max(-self.maxSpeed, max(self.maxSpeed, speed))
        if (abs(speed) > self.maxSpeed):
            if (speed > 0):
                speed = self.maxSpeed
            else:
                speed = -self.maxSpeed

        if self.verbose:
            print("----------------------------------------------")
        logging.info("----------------------------------------------")
        return speed