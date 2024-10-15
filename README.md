
# SARII-TutoredProjectCobotUR3

This project allows you to control a **UR3 Cobot** equipped with a **Robotiq Two-Finger Gripper** using Python via an Ethernet connection. It includes a graphical user interface (GUI) built with **Tkinter** for controlling the cobot and gripper, viewing joint and TCP positions, and configuring movement settings.

## Features

- Control the **UR3 Cobot** with precise joint and TCP movements.
- Operate the **Robotiq Gripper** with commands to open, close, or set a custom position.
- Built-in **security checks** for velocity and acceleration limits to ensure safe operations.
- Includes a **graphical user interface (GUI)** to monitor and control the robot, built with Tkinter.
- Compatible with both **Windows** and **Linux** (MacOS is not supported).
- Option to switch between light and dark themes for the GUI.
- Connect to the robot using an Ethernet connection, with support for setting custom IP addresses.

## Getting Started

### Prerequisites

Make sure you have the following prerequisites installed:

- **Python between version 3.8+ and 3.11-**
- Required Python libraries:
  - `URBasic`
  - `urx`
  - `numpy`
  - `tkinter`
  
You can install the required libraries using the following command:
Note: URBasic is already in the src folder and will not be installed with the following command.

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/SARII-TutoredProjectCobotUR3.git
   ```

2. Install the required libraries using the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. Connect the **UR3 Cobot** and **Robotiq Gripper** to your computer using an Ethernet cable.

4. Run the Python script to launch the application:

   ```bash
   python main.py
   ```

## How to Use

- **Get Joint Angles**: Retrieve the current angles of the UR3 joints.
- **Get TCP Pose**: Retrieve the current Tool Center Point (TCP) position of the UR3.
- **Move Joint**: Send commands to move the UR3 based on the specified joint angles.
- **Move TCP**: Send commands to move the UR3 based on the TCP pose.
- **Gripper Control**: Open, close, or set a custom position for the Robotiq gripper.
- **Theme Switch**: Toggle between light and dark themes in the GUI.
- **Home Position**: Move the UR3 Cobot to the predefined home position.
- **Notice**: Access the included documentation file (.pdf).

## GUI Overview

The graphical interface allows users to control the UR3 Cobot and Robotiq Gripper through easy-to-use buttons and input fields. The main sections include:

- **Joint Angles & TCP Position**: Displays the current joint angles and TCP pose and allows users to set new positions.
- **Movement Controls**: Choose between MoveJ, MoveL, and MoveC commands for moving the robot.
- **Gripper Controls**: Control the gripper by opening, closing, or setting a custom position (0-255).
- **Connection Status**: Shows the current connection state of the robot.
- **Additional Controls**: Access the home position, switch GUI themes, and open the documentation file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Authors

- **Paul Bruno** and **Alexis Pele**  
  Alternants Siemens - Licence Pro SARII, IUT de Bordeaux  
  Promotion 2022-2023  

Version: 1.0 - Glowing Turtle
