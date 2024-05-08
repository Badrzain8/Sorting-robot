#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, ImageFile, SoundFile, Button
from pybricks.tools import wait
import time
from time import sleep
from time import gmtime
from time import localtime

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
# elbow_motor.control.limits(speed=1000, acceleration=300)  # this can be changed later
# base_motor.control.limits(speed=1000, acceleration=300)   # this can be changed later)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the items are in the right position.
elbow_sensor = ColorSensor(Port.S2)

#---------------------------------------------------------------#

# Resets the arm's elbow position. Touches the bottom.
elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=20)
print(elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=20))

# Close gripper if not closed
gripper_motor.run_until_stalled(100, then=Stop.COAST, duty_limit=50)

# Resets elbow_motor angle to zero so we can use it later.
elbow_motor.reset_angle(0)
print(elbow_motor.angle())
elbow_motor.hold()

# Moves up 60 degrees.
elbow_motor.run_angle(100, 60, then=Stop.HOLD)

# Set up the base motor, make it turn all the way to the right
# until the touch sensor is pressed and then reset the base motor
# angle to 0 and hold it in that position.
base_motor.run(-300)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()


# Set up the gripper, make the claw close and set that as 0 angle
# then open it with 90 degrees to make it ready to grab the items.
gripper_motor.run_until_stalled(100, then=Stop.HOLD, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(150, -90)


def color_func():
    ret_col = None
    color = elbow_sensor.rgb()
    print(color)
    if color[0] > 16 and color[1] <= 10 and color[2] < 10:
    #if color[0] > color[1] and color[0] > color[2]:
        ret_col = "Red" 
        ev3.screen.draw_text(50, 50, "Red")
        # ev3.speaker.play_file(SoundFile.RED)
        wait(200)
        ev3.screen.clear()

    elif color[0] < 13 and color[1] > 10 and color[2] < 15:
    #elif color[1] > color[0] and color[1] > color[2]:
        ret_col = "Green"
        ev3.screen.draw_text(50, 50, "Green")
        # ev3.speaker.play_file(SoundFile.GREEN)
        wait(200)
        ev3.screen.clear()

    elif color[0] < 10 and color[1] < 20 and color[2] > 18:
    #elif color[2] > color[0] and color[2] > color[1]:
        ret_col = "Blue"
        ev3.screen.draw_text(50, 50, "Blue")
        # ev3.speaker.play_file(SoundFile.BLUE)
        wait(200)
        ev3.screen.clear()

    elif color[0] > 20 and color[1] >= 10 and color[2] < 20:
        ret_col = "Yellow"
        ev3.screen.draw_text(50, 50, "Yellow")
        # ev3.speaker.play_file(SoundFile.YELLOW)
        wait(200)
        ev3.screen.clear()

    else:
        ret_col = None
        ev3.screen.draw_text(30, 50, "Nothing found")
        # ev3.speaker.play_file(SoundFile.UH_OH)
        wait(200)
        ev3.screen.clear()
    print(ret_col)
    return ret_col


def robot_pick(position):
    # In this function, the base motor makes the arm moves to the deignated
    # pick-up location and then lower the elbow and close up the gripper to
    # grab the item and raise it up to the level of colour sensor.
    
    # Rotate to the pick-up location.
    base_motor.run_target(300, position)
    
    # Lower the arm elbow.
    elbow_motor.run_until_stalled(-20, then=Stop.HOLD, duty_limit=10)
    #elbow_motor.run_target(-60, 0)

    # Close the gripper to grab the item.
    gripper_motor.run_until_stalled(250, then=Stop.HOLD, duty_limit=50) 

    # Raise the arm to lift the item up to the level of colour sensor.
    elbow_motor.run_angle(50, 20, then=Stop.HOLD)

    # Slowly raise the arm til the color sensor senses the color.
    while color_func() == None and elbow_motor.angle() < 80:
        elbow_motor.run(10)
        if elbow_motor.angle() > 70 and gripper_motor.angle() > -35:
            gripper_motor.run_target(100, -90)
        #if gripper_motor.angle() > -5:
            #gripper_motor.run_target(100, -90)
            robot_pick(MIDDLE)
    
    elbow_motor.hold()

# _______* this have been replaced with another well working function and can be removed later.
    # elbow_motor.run_target(50, 60)
    # elbow_sensor.rgb()
    # if color_func() == None:
    #     elbow_motor.run_target(50, 5)
    #     gripper_motor.run_target(50, 90)
    # elif color_func() != None:
    #     elbow_motor.run_target(50, 15)
    
    # if ColorSensor.color() == None:
    #     elbow_motor.run_target(50, 5)
    #     gripper_motor.run_target(50, 90)

def robot_release(position):
    # In this function, the base rotate the arm to the calibrated drop-off zone
    # for that specific colour the item has and then it lower the arm elbow and 
    # open the gripper to release the item in that position.

    # Rotate to the drop-off position designated to that specific colour of the picked up item.
    base_motor.run_target(300, position)
    
    # Lower the arm elbow to release the item on the specified position.
    elbow_motor.run_until_stalled(-20, then=Stop.HOLD, duty_limit=20) # Release in elevated positions
    # elbow_motor.run_target(60, -20) # var (20, -20)

    # Open the gripper to release the item.
    gripper_motor.run_target(100, -90)

    # Raise the arm.
    elbow_motor.run_target(150, 60) #var (60, 0)

# Calibrated position angles for the base motor. 
# Can be changed based on customer needs.
LEFT_LEFT=210
LEFT=165
MIDDLE=115
RIGHT=15
TRASH=60

# Dictionary to store the release position for each colour.
dict_release = {
    "Red" : RIGHT,
    "Blue" : LEFT_LEFT,
    "Yellow" : LEFT,
    }

buttons = {
    0 : Button.UP,
    1 : Button.LEFT,
    2 : Button.CENTER,
    3 : Button.RIGHT,
    4 : Button.DOWN,
    5 : Button.LEFT_UP,
}

# Fixa senare att vi ska kunna programmera in själva med knappar
#count = 0
level = 0

#----------------------------Emergancy-----------------------------------#

# Initiera knapparna och ljudet
# btn = Button()

# Variabel för att hålla reda på om nödläget är aktivt eller inte
emergency_active = False

# Funktion som ska köras när nödknappen trycks
def emergency_action():
    global emergency_active
    print("Nödläge aktiverat!")
    emergency_active = True

# Funktion som återgår till normalt tillstånd när nödknappen trycks igen
def reset_emergency():
    global emergency_active
    print("Nödläge avaktiverat.")
    emergency_active = False

# Huvudloop
# while True:
#     if Button.UP in ev3.buttons.pressed():
#         # Kolla om övre knappen är tryckt
#         if not emergency_active:
#             emergency_action()
#         else:
#             reset_emergency()
#         # Vänta tills knappen släpps för att undvika flera upprepade tryckningar
#         while Button.UP in ev3.buttons.pressed():
#             sleep(0.1)
#     sleep(0.1)  # Sov för att undvika hög CPU-användning


# The main loop for the robot to pick up and release the items.
while True:

    # PLAN för skärm
    # Working Hours
    # Manual Setup
    # Emergency Button (later, easy)

    # A while buttons dict are between 0-5 then the instructions go?
    # Then a level variable. 
    # Level 0 = Working Hours
    # Level 1 = Manual Setup

    

    # # Working Hours - User adds up 1, 2, 3 to desired time
    # tid = 0
    # ev3.screen.draw_text(50, 50, "Choose Time:")
    # ev3.screen.draw_text(50, 50, "UP adds 1")
    # ev3.screen.draw_text(50, 50, "LEFT -> 2")
    # ev3.screen.draw_text(50, 50, "RIGHT -> 3")
    # wait(2000)
    # ev3.screen.clear()

    #time.gmtime(0) # <-- Lösning för working hours

    # if Button.UP in ev3.buttons.pressed():
    #     ev3.speaker.play_file(SoundFile.CONFIRM)

    # btn = Button()
    # buttons = brick.buttons()
    # if Button.LEFT in buttons:
    #     brick(Color.GREEN)
    # elif Button.CENTER in buttons:
    #     brick(Color.YELLOW)
    # elif Button.RIGHT in buttons:
    #     brick(Color.RED)
    if Button.UP in ev3.buttons.pressed():
        # Kolla om övre knappen är tryckt
        if emergency_active == True:
            emergency_action()
        else:
            reset_emergency()
        # Vänta tills knappen släpps för att undvika flera upprepade tryckningar
        while Button.UP in ev3.buttons.pressed():
            sleep(0.1)
    sleep(0.1)  # Sov för att undvika hög CPU-användning


    robot_pick(MIDDLE)
    while color_func() != None:
        if color_func() == "Red":
            robot_release(dict_release["Red"])
            robot_pick(MIDDLE)
            # count += 1
        elif color_func() == "Blue":
            robot_release(dict_release["Blue"])
            robot_pick(MIDDLE)
            # count += 1
        elif color_func() == "Yellow":
            robot_release(dict_release["Yellow"])
            robot_pick(MIDDLE)
            # count += 1
        else:
            robot_release(TRASH)
            robot_pick(MIDDLE)

    # to be continued...
    

