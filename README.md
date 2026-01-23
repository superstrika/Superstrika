# Superstrika - RoboCup Junior Soccer Robot

This project contains the software for the **Superstrika** robot, developed by the RoboCup team from **Gvanim School (Ein Shemer)**. The robot is designed for the **RoboCup Junior Soccer** competition, specifically focusing on autonomous movement and camera-based ball tracking (football cam).

The system runs on a **Raspberry Pi 4 (4GB RAM)** using **ROS 2 Humble**.

## 🏆 RoboCup Junior Soccer
The robot is built to compete in the RoboCup Junior soccer league. The primary goal is to create a fully autonomous robot capable of:
- Locating a specialized IR or color-based ball using a camera system.
- Navigating an omnidirectional field using a 4-wheel drive system.
- Implementing strategic movement to score goals while avoiding obstacles.

---

## 🏗 Project Architecture & Code Model

The project is designed with a clear separation between hardware abstraction and the ROS 2 communication layer. This modularity allows the core robot logic to be reused or tested independently of ROS.

### The "Code Model"
Our design philosophy follows a two-tier approach:
1.  **Hardware Abstraction Classes**: For every physical component (Motors, Servos, Gyro, Screen), we create a dedicated Python class that handles low-level GPIO/I2C communication.
2.  **ROS 2 Node Wrappers**: We then wrap these classes into ROS 2 nodes. The nodes handle subscriptions, publications, and integration into the larger robot ecosystem.

> This structure ensures that if we decide to move away from ROS in the future, the core hardware control logic remains intact and easily portable.

### Directory Structure & Components
- **`src/my_robot_package`**: The main ROS 2 package containing hardware nodes and robot logic.
  - `motor.py` / `motorNode.py`: 4-wheel omnidirectional movement using PWM (via `gpiozero` and `pwm7046`).
  - `servo.py` / `servoNode.py`: Precise servo angle control for robot mechanisms.
  - `screenNode.py`: 20x4 I2C LCD display handling for real-time debugging.
  - `Gyro.py`: BNO055/MPU6050 integration for orientation and stability.
  - `pidCalc.py`: PID control logic for smooth and accurate movement.
  - `UartNode.py` / `UartNoNode.py`: UART communication handling for external sensors or controllers.
  - `VCNL_4040/`: Drivers for proximity and ambient light sensing.
- **`connection/`**: A custom socket-based communication directory. This serves as the main communication between the two robots, allowing for direct client-server command execution over the network.
  - `server.py` / `client.py`: High-speed socket communication layer.
  - `commandManager.py`: Parsing and routing of remote commands.

---

## ❤️ Special Thanks

A huge thank you to the following people who helped make this project possible:

- **[Gal Arbel](https://github.com/galarb)** - For mentorship and technical guidance.
- **[Tomer Ozer](https://github.com/TomerOzer)** - For support in system architecture.
- **[Yoav Aharoni](https://github.com/teddybearpc)** - For hardware and electronic expertise.
- **[Noam Ron](https://github.com/NoamRon1)** - Lead developer and team captain.

---

## 🛠 Setup & Troubleshooting

### Permissions
If you encounter permission errors when using Visual Studio Code (especially inside a container), run:
```bash
sudo chown -R $USER:$USER /home/kev/cubie-1
```

### ROS 2 Environment
If ROS 2 commands are not detected, ensure your environment is sourced:
```bash
source /opt/ros/humble/setup.sh
```

---

*Maintained by the Superstrika Team.*
