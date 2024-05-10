# Welcome to GitHub Desktop!

PA1473 - Software Development: Agile Project
# Robotic Arm Project

## Introduction
This is a software development project focusing on Agile methodologies. The project is about robotic arm control, aimed at sorting and distributing items to different pre-existing zones. The system utilizes Python programming language and is designed to run on a LEGO Mindstorms EV3 robotic platform.

The key features of the project include:
- Implementing functionalities for picking up, sorting, and releasing items based on pre-existing criteria.
- Providing a user-friendly interface for remote control and monitoring of the robotic arm.
- Manually being able to pick three out of four colours [Red, Blue, Yellow, Green] to get sorted.
- Being able to pick out one zone for each colour, including a pick-up zone.

## Getting started
To set up the project and start developing:

1. **Install Python 3.x**: You can download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Installing Software**: Install the required Python libraries using pip:
   pip install ev3dev2

3. **Clone Code**: Using git clone https://github.com/Badrzain8/Sorting-robot.git
  Clone the following:
  - Sorting robot main.py (Main code)
  - client_side.py (Belt Communication)
4. **Download the scripts**: Connect the device to your computer and proceed to download all relevant files.
5. **If Belt (pair via bluetooth)**:
    - Set to powered and visible on both in 'Bluetooth'.
    - Start scan
    - Find the ev3 name (rename if there are multiple robots in the vicinity)
    - Pair and do not proceed to connect.
6. Run.

## Building and running
### Dashboard
1. Start the robot.
2. Choose if you want to communicate with another robot.
(Now you've entered the dashboard. If you skip working hours the robot starts immediately.)
4. Choose the options that suits you, then press start. (Sorting zones are from left to right)
5. Then, if you chose belt, start up the belt running (client_side.py) now.
6. Else, place the items at the pick-up zones and let it sort the items for you!

## Features
- [x] US_1(B): As a user I want the robot to pick up items (LEGO blocks) from one designated position.
- [x] US_2(B): As a user I want the robot to sort and drop off the items in assigned locations.
- [x] US_03: As a user I want the robot to check and determine if an item is present at a specific location.
- [x] US_04(B): As a user I want the robot to identify the color of the item using the color sensor.
- [x] US_05: As a user I want the robot to sort and drop the items off at the assigned locations based on their colors.
- [x] US_06: As a user I want the robot to be able to pick up items from different height levels.
- [x] US_08: As a user I want to calibrate maximum of three colors and assign specific locations for every calibrated color.
- [x] US_09: As a user I want the robot to check the pick-up zone periodically to see if a new item has arrived.
- [x] US_10: As a user I want the robot to to work within assigned working hours which can be changed by the user.
- [ ] US_11: As a user I want the robot to be able to communicate with other robots to work together.
- [x] US_12: As a user I want to assign 1 pick-up and 2 different drop-off zones (position and heights) by using the buttons.
- [ ] US_13: As a user I want to be able to easily reprogram the locations and zones
- [x] US_14: As a user I want the robot to have the ability to change the working hours by the user manually.
- [ ] US_15: As a user I want the robot to have an emergency button to terminate all operations immediately and safely.
- [x] US_16: As a user I want the robot to pick up and drop off an item at an assigned location within a short time (5 sec)
- [ ] US_17: As a user I want the arm to pick up bricks from a conveyor belt sorting by colors and form via bluetooth.
- [ ] US_18: As a user I want the robot to have a pause button.
- [x] US_19: As a user I want the robot to have a dashboard for manual setup.


PA1473 - Software Development: Agile Project
# Robotic Arm Project

## Introduction
This is a software development project focusing on Agile methodologies. The project is about robotic arm control, aimed at sorting and distributing items to different pre-existing zones. The system utilizes Python programming language and is designed to run on a LEGO Mindstorms EV3 robotic platform.

The key features of the project include:
- Implementing functionalities for picking up, sorting, and releasing items based on pre-existing criteria.
- Providing a user-friendly interface for remote control and monitoring of the robotic arm.
- Manually being able to pick three out of four colours [Red, Blue, Yellow, Green] to get sorted.
- Being able to pick out one zone for each colour, including a pick-up zone.

## Getting started
To set up the project and start developing:

1. **Install Python 3.x**: You can download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Installing Software**: Install the required Python libraries using pip:
   pip install ev3dev2

3. **Clone Code**: Using git clone https://github.com/Badrzain8/Sorting-robot.git
  Clone the following:
  - Sorting robot main.py (Main code)
  - client_side.py (Belt Communication)
4. **Download the scripts**: Connect the device to your computer and proceed to download all relevant files.
5. **If Belt (pair via bluetooth)**:
    - Set to powered and visible on both in 'Bluetooth'.
    - Start scan
    - Find the ev3 name (rename if there are multiple robots in the vicinity)
    - Pair and do not proceed to connect.
6. Run.

## Building and running
### Dashboard
1. Start the robot.
2. Choose if you want to communicate with another robot.
(Now you've entered the dashboard. If you skip working hours the robot starts immediately.)
4. Choose the options that suits you, then press start. (Sorting zones are from left to right)
5. Then, if you chose belt, start up the belt running (client_side.py) now.
6. Else, place the items at the pick-up zones and let it sort the items for you!

## Features
- [x] US_1(B): As a user I want the robot to pick up items (LEGO blocks) from one designated position.
- [x] US_2(B): As a user I want the robot to sort and drop off the items in assigned locations.
- [x] US_03: As a user I want the robot to check and determine if an item is present at a specific location.
- [x] US_04(B): As a user I want the robot to identify the color of the item using the color sensor.
- [x] US_05: As a user I want the robot to sort and drop the items off at the assigned locations based on their colors.
- [x] US_06: As a user I want the robot to be able to pick up items from different height levels.
- [x] US_08: As a user I want to calibrate maximum of three colors and assign specific locations for every calibrated color.
- [x] US_09: As a user I want the robot to check the pick-up zone periodically to see if a new item has arrived.
- [x] US_10: As a user I want the robot to to work within assigned working hours which can be changed by the user.
- [ ] US_11: As a user I want the robot to be able to communicate with other robots to work together.
- [x] US_12: As a user I want to assign 1 pick-up and 2 different drop-off zones (position and heights) by using the buttons.
- [ ] US_13: As a user I want to be able to easily reprogram the locations and zones
- [x] US_14: As a user I want the robot to have the ability to change the working hours by the user manually.
- [ ] US_15: As a user I want the robot to have an emergency button to terminate all operations immediately and safely.
- [x] US_16: As a user I want the robot to pick up and drop off an item at an assigned location within a short time (5 sec)
- [ ] US_17: As a user I want the arm to pick up bricks from a conveyor belt sorting by colors and form via bluetooth.
- [ ] US_18: As a user I want the robot to have a pause button.
- [x] US_19: As a user I want the robot to have a dashboard for manual setup.


