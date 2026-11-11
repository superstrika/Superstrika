# Superstrika

Software for the **Superstrika** RoboCup Junior Soccer robot, developed by the team at **Gvanim School (Ein Shemer)**. The project runs on a Raspberry Pi and brings together robot movement, sensor input, ball detection, and match behaviour.

## What it does

- Drives a four-wheel omnidirectional base.
- Uses a camera model to detect the ball and goals.
- Reads hardware such as the MPU6050 gyro, VCNL4040 proximity sensor, line sensors, servo, dribbler, and kicker.
- Provides hunter behaviour, movement control with PID correction, calibration tools, and hardware tests.

## Related repositories

| Repository | What it is |
|---|---|
| [superstrika/Superstrika](https://github.com/superstrika/Superstrika) | **This repository**: the current robot code (formerly `Superstrika-new`, which still redirects here) |
| [superstrika/simulator](https://github.com/superstrika/simulator) | 2D RoboCupJunior Soccer simulator that can run this repository's robot code unchanged |
| [superstrika/Superstrika-old](https://github.com/superstrika/Superstrika-old) | The previous, ROS 2 based code base, kept for reference |

## Simulator

The [Superstrika simulator](https://github.com/superstrika/simulator) (`rcj_sim`) is a 2D top-down simulator for RoboCupJunior Soccer, written in Python with pygame and pymunk. It models the official 2026 field, ball and goals, a Ø 18 cm robot with four X-mounted omni wheels, a 360° and a front camera, dribbler, kicker, 16 line sensors and a gyro, and has an automatic referee with `free`, `basic` and `full` rule modes. You can watch matches live, pause and step, drag the ball and robots around, or run headless matches for quick tests. Standalone builds for Windows, Linux and macOS are published from its GitHub Actions, so no Python install is needed to try it.

Its `superstrika/` folder runs **our real `robot/hunter.py` unchanged**. Only the hardware layer is replaced: `gpiozero`/`smbus2` are faked, `motor7046` drives the simulated omni wheels, `MPU6050` reads the simulated heading, `WebCamera` becomes a simulated camera on the tilt servo, and `time.time()`/`time.sleep()` run on simulation time. This makes it a quick way to test behaviour changes before putting them on the robot.

To run our code in the simulator, clone it next to this repository and point it at this checkout:

```bash
git clone https://github.com/superstrika/simulator.git
cd simulator
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
SUPERSTRIKA_PATH=../Superstrika .venv/bin/python -m rcj_sim superstrika/match.yaml
```

Without `SUPERSTRIKA_PATH` the bridge looks for `../Superstrika-new`. The motor speed, camera and servo values it assumes are in `SETTINGS` in `superstrika/superstrika_bridge.py`. See the simulator's [Superstrika README](https://github.com/superstrika/simulator/blob/main/superstrika/README.md) for what is simulated, the calibration assumptions, and the issues it found in `hunter.py`.

## Previous code base

[Superstrika-old](https://github.com/superstrika/Superstrika-old) holds the earlier version of the robot software (its last code change, in May 2026, was the hunter code for that tournament). It was built as a ROS 2 package (`src/my_robot_package`, built with colcon) with motor, servo, UART and screen nodes, used `pigpio` for GPIO, had a network client/server for controlling the robot from a laptop (`connection/`), and MicroPython code for ESP32 boards running the kicker and motors (`esp32/`). Many of the drivers here (motor, gyro, VCNL4040, TCRT5000, servo, dribbler, kicker, PID, edge-line detection) started there. It is no longer maintained; new work belongs in this repository.

## Dependencies installation

1. Install the system dependencies:

   ```bash
   sudo apt update
   sudo apt install neovim build-essential swig python3-dev liblgpio-dev
   ```

2. Create a virtual environment if one does not already exist:

   ```bash
   python3 -m venv venv
   ```

3. Activate it:

   ```bash
   source venv/bin/activate
   ```

4. Install the project requirements:

   ```bash
   pip3 install -r robot/requirements.txt
   ```

5. Install the vision packages:

   ```bash
   pip3 install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu ultralytics torch torchvision
   ```

## Running with Docker

The Docker image holds only the dependencies. The code is bind-mounted from this repo, so editing it on the Pi only needs a container restart. GitHub Actions rebuilds the image (`ghcr.io/superstrika/superstrika-new`) when `Dockerfile`, `constraints.txt` or `robot/requirements.txt` change.

Set up a new Pi (Docker installed, I2C/SPI/UART enabled in `raspi-config`):

```bash
git clone https://github.com/superstrika/Superstrika.git
cd Superstrika
docker compose pull
docker compose up -d
```

`robot-core` runs `main.py` and starts again automatically after a reboot. Everyday commands:

```bash
docker compose restart robot-core     # after editing code
docker compose logs -f robot-core     # watch output
docker compose up -d console          # start the web console (manual only, http://<pi>:8080)
docker compose stop console           # stop the web console
docker compose run --rm robot-core python3 -m robot.calibration.servo_calibration
```

The console launches `main.py` itself, so stop `robot-core` before using it to keep two processes off the same hardware.

## Project structure

```text
.
├── main.py                 # Selects and starts the current robot entry point
├── Dockerfile              # Dependency-only robot image
├── docker-compose.yaml     # robot-core and console services
├── constraints.txt         # Pinned versions for the Docker build
├── .github/workflows/      # Builds and pushes the Docker image
├── robot/
│   ├── hunter.py           # Main attacking (hunter) behaviour
│   ├── keeper.py           # Goalkeeper behaviour
│   ├── joy_ride.py         # Manual movement sequence for testing
│   ├── components/         # Hardware drivers: motors, cameras, gyro, sensors, servo, kicker
│   ├── processes/          # Higher-level control: multi-motor drive, PID, gyro movement, line detection
│   ├── consts/             # Robot configuration, pins, constants, and enums
│   ├── models/             # ONNX models used for vision detection
│   ├── calibration/        # Motor and servo calibration scripts
│   ├── tests/              # Focused hardware and camera test scripts
│   ├── PIDAnalysis/        # PID logging and analysis utilities
│   ├── console/            # Local web console and its configuration
│   └── requirements.txt    # Python dependencies
├── rp2040-zero/            # PlatformIO project for the Waveshare RP2040-Zero (early stage)
├── mirror/                 # Hyperbolic mirror calculations (notebook) and DXF drawing
├── startup/                # systemd service for running the web console without Docker
└── log/                    # Runtime log output
```

## Configuration and running

Hardware pins, sensor settings, camera dimensions, and game options are defined in `robot/consts/data.py`. The main application entry point is `main.py`; choose the behaviour or test you want to run there, then start it from the repository root:

```bash
python3 main.py
```

Useful standalone scripts include:

```bash
python3 -m robot.calibration.motor_identification
python3 -m robot.calibration.servo_calibration
python3 -m robot.tests.captureRaspiFrame
python3 -m robot.tests.captureWebFrames
```

To inspect devices connected to the Raspberry Pi I2C bus:

```bash
sudo i2cdetect -y 1
```

## Special thanks

- [Gal Arbel](https://github.com/galarb) — Team mentor
- [Tomer Ozer](https://github.com/TomerOzer) — Team member
- [Yoav Aharoni](https://github.com/teddybearpc) — Team member
- [Noam Ron](https://github.com/NoamRon1) — Team member
- [Itamar Hoter Ishai](https://github.com/itamarhoter) — Team member

*Maintained by the Superstrika Team.*
