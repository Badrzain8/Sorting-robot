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
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_sensor = ColorSensor(Port.S2)

CALIBRATED_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
#CALIBRATED_POSITIONS = [LEFT_LEFT=200, LEFT=160, MIDDLE=100, RIGHT=40]
#---------------------------------------------------------------#
while elbow_sensor.reflection() < 35:
    elbow_motor.run_angle(-10, 15)
# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(25, 1000)  #(25, 1300) var innan
elbow_motor.run(30) # var 50
if elbow_sensor.reflection() < 20:
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-30)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(150, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(100, -90)

def sense_object_colour():
    color = None
    if elbow_sensor.color() == Color.RED:
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
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.

    # Rotate to the pick-up position.
    base_motor.run_target(100, position)
    # Lower the arm.
    elbow_motor.run_target(20, -20)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(150, then=Stop.HOLD, duty_limit=50)

    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(50, 20)
    #wait(100)
    #sense_object_colour()

def robot_release(position):
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.

    # Rotate to the drop-off position.
    base_motor.run_target(60, position)
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(20, -10)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(50, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 0)

# def robot_check(position):
    # Rotate to the drop-off position.
    # base_motor.run_target(60, position)

    # Lower the arm to put the wheel stack on the ground.
    # elbow_motor.run_target(20, -10)

"""
# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)
"""
# This is the main part of the program. It is a loop that repeats endlessly.
#
# First, the robot moves the object on the left towards the middle.
# Second, the robot moves the object on the right towards the left.
# Finally, the robot moves the object that is now in the middle, to the right.

# Now we have a wheel stack on the left and on the right as before, but they
# have switched places. Then the loop repeats to do this over and over.

LEFT_LEFT=200
LEFT=160
MIDDLE=100
RIGHT=0

dict_release = {
    "Red" : MIDDLE,
    "Blue" : LEFT_LEFT,
    "Yellow" : LEFT,
    }

count = 0

def getlightvalue():
    light = elbow_sensor.reflection()
    while True:
        print(light)
    return light


# program körs
while True:

    while count <= 2:
        # robot_pick(RIGHT)
        getlightvalue()
        for i in dict_release:
            if sense_object_colour() == i:
                robot_release(dict_release[i])
                robot_pick(RIGHT)
                count += 1
            #else:
                #robot_release(RIGHT)
    robot_release(RIGHT)
    exit()

    """
    for i in dict_release:
    robot_pick(RIGHT)
    if sense_object_colour() == i:
        robot_release(dict_release[i])
    """

    # Move a wheel stack from the left to the middle.
    # robot_pick(RIGHT)
    # robot_release(MIDDLE)
    # robot_pick(RIGHT)
    # robot_release(LEFT)
    # robot_pick(RIGHT)
    # robot_release(LEFT_LEFT)

    # Move a wheel stack from the right to the left.
    #robot_pick(RIGHT)
    #robot_release(LEFT)

    # Move a wheel stack from the middle to the right.
    #robot_pick(MIDDLE)
    #robot_release(RIGHT)


