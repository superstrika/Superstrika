from motor import motor7046

def main() -> None:
    motor1 = motor7046(19, 20, switch=True) # green
    motor2 = motor7046(21, 22, switch=False) # white
    motor3 = motor7046(23, 24, switch=False) # orange
    motor4 = motor7046(25, 6, switch=True) # orange

    motors: motor7046 = [motor3, motor1, motor2, motor4]
    speeds = motor1.calculate_speed(0, 70, 0)

    print(speeds)
    for i in range(len(speeds)):
        motors[i].speed = speeds[i]
        print(f"Running motor {i} on value: {speeds[i]}")
        input()
        motors[i].speed = 0


if __name__ == "__main__":
    main()