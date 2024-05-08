#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, ImageFile, SoundFile
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)  # this can be changed later
base_motor.control.limits(speed=60, acceleration=120)   # this can be changed later

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the items are in the right position.
elbow_sensor = ColorSensor(Port.S2)
#---------------------------------------------------------------#

# CALIBRATED_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
#CALIBRATED_POSITIONS = [LEFT_LEFT=200, LEFT=160, MIDDLE=100, RIGHT=40]


while elbow_sensor.reflection() < 35:
    elbow_motor.run_angle(-10, 15)
elbow_motor.run_time(25, 1000)  #(25, 1300) var innan
elbow_motor.run(30) # var 50
if elbow_sensor.reflection() < 20:
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Set up the base motor, make it turn all the way to the right
# until the touch sensor is pressed and then reset the base motor
# angle to 0 and hold it in that position.
base_motor.run(-30)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# set up the grippier, make the clow close and set that as 0 angle
# then open it with 90 degrees to make it ready to grab the items.
gripper_motor.run_until_stalled(150, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(100, -90)

def sense_object_colour():
    color = None
    if elbow_sensor.rgb() == Color.RED:
        color = "Red"
        for _ in range(4):
            ev3.speaker.beep()
            wait(100)
    elif elbow_sensor.color() == Color.YELLOW:
        color = "Yellow"
        for _ in range(3):
            ev3.speaker.beep()
            wait(100)
    elif elbow_sensor.color() == Color.GREEN:
        color = "Green"
        for _ in range(2):
            ev3.speaker.beep()
            wait(100)
    elif elbow_sensor.color() == Color.BLUE:
        color = "Blue"
        for _ in range(1):
            ev3.speaker.beep()
            wait(100)
    else:
        color = None
        
    return color


def robot_pick(position):
    # in this function, the base motor makes the arm moves to the deignated
    # pick-up location and then lower the elbow and close up the gripper to
    # grab the item and raise it up to the level of colour sensor.

    # Rotate to the pick-up location.
    base_motor.run_target(100, position)
    # Lower the arm elbow.
    elbow_motor.run_target(20, then=Stop.COAST, duty_limit=50)
    # Close the gripper to grab the item.
    gripper_motor.run_until_stalled(150, then=Stop.HOLD, duty_limit=50)

    # Raise the arm to lift the item up to the level of colour sensor.
    elbow_motor.run_target(50, 15)

    # if ColorSensor.color() == None:
    #     elbow_motor.run_target(50, 5)
    #     gripper_motor.run_target(50, 90)
  
    #wait(100)
    #sense_object_colour()

def robot_release(position):
    # In this function, the base rotate the arm to the calibrated drop-off zone
    # for that specific colour the item has and then it lower the arm elbow and 
    # open the gripper to release the item in that position.


    # Rotate to the drop-off position designated to that specific colour of the picked up item.
    base_motor.run_target(60, position)
    # Lower the arm elbow to release the item on the specified position.
    elbow_motor.run_target(20, -20) # var (20, -10)
    # Open the gripper to release the item.
    gripper_motor.run_target(50, -90)
    # Raise the arm.
    elbow_motor.run_target(50, 15) #var (60, 0)

# Calibrated position angles for the base motor. 
# Can be changed based on customer needs.
LEFT_LEFT=200
LEFT=160
MIDDLE=100
RIGHT=0

# Dictionary to store the release position for each colour.
dict_release = {
    "Red" : RIGHT,
    "Blue" : LEFT_LEFT,
    "Yellow" : LEFT,
    }

count = 0

# The main loop for the robot to pick up and release the items.
while True:

    while count <= 2:
        robot_pick(MIDDLE)
        # while ColorSensor.color() != Color.RED or ColorSensor.color() != Color.YELLOW or ColorSensor.color() != Color.GREEN or ColorSensor.color() != Color.BLUE:
            # elbow_motor.run_target(50, 5)
            # wait (100)
            # gripper_motor.run_target(50, -90)
              # robot_pick(MIDDLE)
        for i in dict_release:
            if sense_object_colour() == i:
                robot_release(dict_release[i])
                robot_pick(MIDDLE)
                count += 1
            # else:
                # robot_release(RIGHT)
    robot_release(MIDDLE)
    break

    """
    for i in dict_release:
    robot_pick(RIGHT)
    if sense_object_colour() == i:
        robot_release(dict_release[i])
    """

# to be continued...