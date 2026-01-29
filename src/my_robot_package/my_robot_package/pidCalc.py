import time

class PidCalc:
    def __init__(self, kp: float, ki: float, kd: float, maxSpeed: float, maxIntegral: float) -> None:
        self.kp: float = kp
        self.ki: float = ki
        self.kd: float = kd

        self.prevError: float = 0
        self.integral: float = 0

        self.lastTime: float = time.time()

        self.maxSpeed: float = abs(maxSpeed)
        self.maxIntegral: float = abs(maxIntegral)

    def pidCalc(self, error: float) -> float:
        dt = time.time() - self.lastTime


        self.integral += error * dt
        self.integral = max(-self.maxIntegral, min(self.integral, self.maxIntegral))

        derivative = (error - self.prevError) / dt if dt > 0 else 0.0
        speed = self.kp * error + self.ki * self.integral + self.kd * derivative

        self.lastTime = time.time()
        self.prevError = error

        # speed = max(-self.maxSpeed, max(self.maxSpeed, speed))
        if (abs(speed) > self.maxSpeed):
            if (speed > 0):
                speed = self.maxSpeed
            else:
                speed = -self.maxSpeed
        return speed