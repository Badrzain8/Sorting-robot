#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, ImageFile, SoundFile, Button
from pybricks.tools import wait
import time
from time import sleep
from time import gmtime


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
"""
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
        wait(200)
        ev3.screen.clear()

    elif color[0] < 13 and color[1] > 10 and color[2] < 15:
    #elif color[1] > color[0] and color[1] > color[2]:
        ret_col = "Green"
        ev3.screen.draw_text(50, 50, "Green")
        wait(200)
        ev3.screen.clear()

    elif color[0] < 10 and color[1] < 20 and color[2] > 18:
    #elif color[2] > color[0] and color[2] > color[1]:
        ret_col = "Blue"
        ev3.screen.draw_text(50, 50, "Blue")
        wait(200)
        ev3.screen.clear()

    elif color[0] > 20 and color[1] >= 10 and color[2] < 20:
        ret_col = "Yellow"
        ev3.screen.draw_text(50, 50, "Yellow")
        wait(200)
        ev3.screen.clear()

    else:
        ret_col = None
        ev3.screen.draw_text(30, 50, "Nothing found")
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
"""
# Calibrated position angles for the base motor. 
# Can be changed based on customer needs.
LEFT_LEFT=210
LEFT=165
MIDDLE=115
RIGHT=15
TRASH=60

zone_dict = {
    0 : LEFT_LEFT,
    1 : LEFT,
    2 : MIDDLE,
    3 : RIGHT,
}

# Dictionary to store the release position for each colour.
dict_release = {
    "Red" : RIGHT,
    "Blue" : LEFT_LEFT,
    "Yellow" : LEFT,
    }

color_dict = {
    0 : "Red",
    1 : "Blue",
    2 : "Yellow",
    3 : "Green"
    }

active_zones = {

}

buttons = {
    0 : Button.UP,
    1 : Button.LEFT,
    2 : Button.CENTER,
    3 : Button.RIGHT,
    4 : Button.DOWN,
    5 : Button.LEFT_UP,
}

# ---------- Emergancy Stop ------------
def Emergancy_stop():
    print("Emergency stop")
    ev3.speaker.beep()
    base_motor.stop()
    elbow_motor.stop()
    gripper_motor.stop()
    wait(2000)
    exit()
    

# Fixa senare att vi ska kunna programmera in själva med knappar
#count = 0
pickup_zone = False
zones = False
zone_picker = 0
check = False
# pickup_col = None

press_count = 0
time_set = 0
menu = True
menu_done = True
menu_press_count = 0
sorting_zone_menu = 0
center = False
#pickup_zone = False
zone_pickup = 0
p = 0

# The main loop for the robot to pick up and release the items.
while True:
#-----------------Dashboard MENU-------------------------
# Display's x coordinates: 0 - 177
# Display's y coordinates: 0 - 127

    while menu == True:
        if menu_press_count < 0:
            menu_press_count = 0
        elif menu_press_count > 2:
            menu_press_count = -1
        
        # ev3.screen.draw_text(50, 0, "MENU")
        # ev3.screen.draw_text(0, 20, "--> Working Hours")
        # ev3.screen.draw_text(0, 40, "--> Sorting Zones")
        # ev3.screen.draw_text(0, 60, "--> Pick Up Zones")
        # ev3.screen.draw_text(50, 80, "Start")

        if Button.DOWN in ev3.buttons.pressed():
            menu_press_count += 1
        elif Button.UP in ev3.buttons.pressed():
            menu_press_count += -1

        if menu_press_count == 0:
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "--> Working Hours", Color.WHITE, Color.BLACK)
            ev3.screen.draw_text(0, 40, "Sorting Zones")
            ev3.screen.draw_text(50, 60, "Start")
            wait(500)
            if Button.CENTER in ev3.buttons.pressed():
                ev3.screen.clear()
                center = True
            while center == True:
                if Button.UP in ev3.buttons.pressed():
                    time_set += 5
                    wait(200)
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 80, time_set)
                    ev3.screen.draw_text(0, 0, "WORKING HOURS")
                    ev3.screen.draw_text(0, 20, "UP: + 5 sec")
                    ev3.screen.draw_text(0, 40, "DOWN: - 5 sec")
                    ev3.screen.draw_text(0, 60, "LEFT: DONE")
                elif Button.DOWN in ev3.buttons.pressed():
                    time_set -= 5
                    wait(200)
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 80, time_set)
                    ev3.screen.draw_text(0, 0, "WORKING HOURS")
                    ev3.screen.draw_text(0, 20, "UP: + 5 sec")
                    ev3.screen.draw_text(0, 40, "DOWN: - 5 sec")
                    ev3.screen.draw_text(0, 60, "LEFT: DONE")
                elif Button.LEFT in ev3.buttons.pressed():
                    center = False
                ev3.screen.draw_text(0, 80, time_set)
                ev3.screen.draw_text(0, 0, "WORKING HOURS")
                ev3.screen.draw_text(0, 20, "UP: Increase time")
                ev3.screen.draw_text(0, 40, "DOWN: Decrease time")
                ev3.screen.draw_text(0, 60, "LEFT: DONE")
        elif menu_press_count == 1:
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "Working Hours")
            ev3.screen.draw_text(0, 40, "--> Sorting Zones", Color.WHITE, Color.BLACK)
            ev3.screen.draw_text(50, 60, "Start")
            wait(500)
            if Button.CENTER in ev3.buttons.pressed():
                ev3.screen.clear()
                center = True
            while center == True:
                ev3.screen.clear()
                # ev3.screen.draw_text(0, 0, "SORTING ZONES")

                while pickup_zone == False:
                    if p < 0:
                        p = 0
                    elif p > 3:
                        p = 0
                    ev3.screen.draw_text(50, 0, "Pick-Up Zone (CENTER=DONE)")
                    if Button.UP in ev3.buttons.pressed():
                        p += 1
                        wait(200)
                        ev3.screen.clear()
                        ev3.screen.draw_text(50, 0, "Pick-Up Zone (CENTER=DONE)")
                        ev3.screen.draw_text(0, 40, p)
                    elif Button.DOWN in ev3.buttons.pressed():
                        p -= 1
                        wait(200)
                        ev3.screen.clear()
                        ev3.screen.draw_text(50, 0, "Pick Up Zone (CENTER=DONE)")
                        ev3.screen.draw_text(0, 40, p)
                        check = True
                    elif Button.CENTER in ev3.buttons.pressed():
                        ev3.screen.clear()
                        zone_pickup = zone_dict[p]
                        p = 0
                        if check == True:
                            pickup_zone = True

                # if pickup_zone == True:
                #     ev3.screen.draw_text(0, 40, "Pick-Up Zone SET")

                while zones == False:
                    if p < 0:
                        p = 0
                    elif p > 3:
                        p = 0
                    ev3.screen.draw_text(0, 40, "Sorting Zones")
                    while zone_picker < 3:
                        if Button.UP in ev3.buttons.pressed():
                            ev3.screen.draw_text(0, 0, "Zone: (CENTER=DONE)")
                            ev3.screen.draw_text(50, 20, zone_picker + 1)
                            wait(200)
                            ev3.screen.draw_text(0, 40, color_dict[p])
                            p += 1
                            pickup_col = color_dict[p]
                        elif Button.DOWN in ev3.buttons.pressed():
                            ev3.screen.clear()
                            ev3.screen.draw_text(0, 0, "Zone: (CENTER=DONE)")
                            ev3.screen.draw_text(50, 20, zone_picker + 1)
                            wait(200)
                            ev3.screen.draw_text(0, 40, color_dict[p])
                            p -= 1
                            pickup_col = color_dict[p]
                        elif Button.CENTER in ev3.buttons.pressed():
                            ev3.screen.clear()
                            active_zones[zone_picker] = color_dict[p]
                            p = 0
                            zone_picker += 1
                            if zone_picker == 3:
                                zones = True

                        
                # ev3.screen.draw_text(0, 40, "ZONE 1: ")
                # ev3.screen.draw_text(0, 60, "ZONE 2: ")
                # ev3.screen.draw_text(0, 80, "ZONE 3: ")

                # center = False
        elif menu_press_count == 2:
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "Working Hours")
            ev3.screen.draw_text(0, 40, "Sorting Zones")
            ev3.screen.draw_text(50, 60, "--> Start", Color.WHITE, Color.BLACK)
            wait(500)
            if Button.CENTER in ev3.buttons.pressed(): # And rest have been chosen
                ev3.screen.clear()
                menu = False

        # if Button.CENTER in ev3.buttons.pressed():
        #     if menu_press_count == 0:
        #         ev3.screen.clear()
        #         ev3.screen.draw_text(60, 60, "Hej")
        #         wait(500)
        #     elif menu_press_count == 1:
        #         ev3.screen.clear()
        #         ev3.screen.draw_text(60, 60, "Tja")
        #         wait(500)
        #         # enter_sorting_hours = True
        #     elif menu_press_count == 2:
        #         ev3.screen.clear()
        #         ev3.screen.draw_text(60, 60, "Tjena")
        #         wait(500)
        #         # enter_pickup_hours = True
        #     elif menu_press_count == 3 and menu_done == True:
        #         ev3.screen.clear()
        #         ev3.screen.draw_text(60, 60, "Start")
        #         wait(500)
        #         menu == False

#-----------------MENU-------------------------

#-----------------WORKING HOURS-------------------------
    # if Button.LEFT in ev3.buttons.pressed() and press_count == 0:
    #     working_hrs_loop = True
    #     press_count += 1

    # while working_hrs_loop == True:
    #     if Button.RIGHT in ev3.buttons.pressed():
    #         ev3.screen.clear()
    #         time_set += 5 # Seconds, minutes or hours is determined later
    #         ev3.screen.draw_text(50, 50, time_set)
            
    #     if Button.RIGHT in ev3.buttons.pressed() and press_count == 1:
    #         ev3.screen.clear()
    #         working_hrs_loop = False
    #         press_count += 0
#-----------------WORKING HOURS-------------------------
"""
    # Implementera timer funktion
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
"""