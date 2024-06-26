#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, BluetoothMailboxClient 
import time
import threading as th

# The dynamic dictionary that is used for the establishments of positions and colours.
active_zones = {}

emergency_stop = False
belt = False


# Let the worker thread run for a while
time.sleep(5)

# Activate emergency stop
emergency_stop = True

print("Program stopped.")

collaborator = ''

client = BluetoothMailboxClient()

# The server must be started before the client!
me = ['client']
# This is the name of the remote EV3 are connecting to, this can be changed based on the name of the robot.
SERVERID = 'ev3dev-' + collaborator 

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

messages = ['occupied', 'gift4u', 'feed', 'stop', 'emergency', 'free']
# 0 send nothing, 1 for occupied, 2 for gift4u, 3 feed, 4 stop, 5 free.
send = ['nothing']
Em_stop = [False]

# Coms thread.
thread2Alive = [False]
thread_one = th.Thread()

# Initialize the EV3 Brick
ev3 = EV3Brick()

mbox = ""

distributemessages = ['receevied', 'occupied']  #0 : receevied, 1: occupied.
distributelist = [False, False]

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
emergency = False

#-------------------------------FUNCTION DEFINITIONS---------------------------------#

# this function is used to detect the colour of the item.
# The function returns the colour of the item.
# The function uses the RGB sensor to detect the colour of the item.
def color_func():
    ret_col = None
    color = elbow_sensor.rgb()
    print(color)
    if color[0] >= 15 and color[1] <= 10 and color[2] <= 18:
        ret_col = "Red" 
        ev3.screen.draw_text(50, 50, "Red")
        wait(200)
        ev3.screen.clear()
    elif color[0] < 13 and color[1] > 10 and color[2] <= 20:
        ret_col = "Green"
        ev3.screen.draw_text(50, 50, "Green")
        wait(200)
        ev3.screen.clear()
    elif color[0] < 10 and color[1] < 20 and color[2] > 24:
        ret_col = "Blue"
        ev3.screen.draw_text(50, 50, "Blue")
        wait(200)
        ev3.screen.clear()
    elif color[0] > 20 and color[1] >= 10 and color[2] <= 20:
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


# In this function, the base motor makes the arm moves to the deignated
# pick-up location and then lower the elbow and close up the gripper to
# grab the item and raise it up to the level of colour sensor.
def robot_pick(position):
  
    
    # Rotate to the pick-up location.
    base_motor.run_target(300, position)
    
    # Lower the arm elbow.
    elbow_motor.run_until_stalled(-20, then=Stop.HOLD, duty_limit=10)
    #elbow_motor.run_target(-60, 0)

    # Close the gripper to grab the item.
    gripper_motor.run_until_stalled(250, then=Stop.HOLD, duty_limit=70) 

    # Raise the arm to lift the item up to the level of colour sensor.
    elbow_motor.run_angle(50, 20, then=Stop.HOLD)

    # Slowly raise the arm tilL the color sensor senses the color.
    while color_func() == None and elbow_motor.angle() < 80:
        elbow_motor.run(10)
        if elbow_motor.angle() > 70 and gripper_motor.angle() > -35:
            gripper_motor.run_target(80, -75)
            robot_pick(active_zones['Pick-Up Zone'])

    elbow_motor.hold()
        
    # Raise the arm to a higher level to avoid hitting other items while rotating.
    # wait(800)
    # elbow_motor.run_angle(30, 10, then=Stop.HOLD)


# In this function, the base rotate the arm to the calibrated drop-off zone
# for that specific colour the item has and then it lower the arm elbow and 
# open the gripper to release the item in that position.
def robot_release(position):
    
    elbow_motor.run_angle(50, 30, then=Stop.HOLD)

    # Rotate to the drop-off position designated to that specific colour of the picked up item.
    base_motor.run_target(300, position)
    
    # Lower the arm elbow to release the item on the specified position.
    elbow_motor.run_until_stalled(-20, then=Stop.HOLD, duty_limit=10) # Release in elevated positions

    # Open the gripper to release the item.
    gripper_motor.run_target(100, -90)

    # Raise the arm.
    elbow_motor.run_target(150, 60) #var (60, 0)


# In this function, we get the current time and date from the EV3 brick, it differs from the actual time and date.
# and it differs from robot to robot.
# The function returns the current day, hour, minute and seconds.
def time_definitions():
    loc = time.time()
    local = time.localtime(loc)
    "G?"
    # day = local.tm_mday - 22
    # hour = local.tm_hour - 11
    # minute = local.tm_min - 2
    # seconds = local.tm_sec + 37
    "F"
    # day = local.tm_mday + 4
    # hour = local.tm_hour - 4
    # minute = local.tm_min + 11
    # seconds = local.tm_sec - 10
    "D"
    # day = local.tm_mday - 14
    # hour = local.tm_hour + 6
    # minute = local.tm_min - 7
    # seconds = local.tm_sec
    "B"
    day = local.tm_mday
    hour = local.tm_hour + 2
    minute = local.tm_min
    seconds = local.tm_sec

    if hour < 0:
        hour += 24
    elif hour > 24:
        hour -= 24
    if local.tm_hour == 0:
        day -= 1
        hour += local.tm_hour - 11
    if seconds > 59:
        minute += 1
        seconds = 0
    elif seconds < 1:
        seconds = 0
    elif minute > 59:
        hour += 1
        minute = 0
    elif hour > 24:
        day += 1
        hour = 0
    elif hour < 0:
        hour = 0
    
    print(day, hour, minute, seconds)
        
    return day, hour, minute, seconds


# this function will stop all the motors and clear the screen to show the message "PAUSED".
def robot_pause():
    ev3.screen.clear()
    ev3.screen.draw_text(50, 50, "PAUSED")
    # wait(2000)
    base_motor.stop()
    elbow_motor.stop()
    gripper_motor.stop()
    ev3.screen.clear()
    
# this function will run all the motors and clear the screen to show the message "RESUMING".
def robot_resume():
    ev3.screen.clear()
    ev3.screen.draw_text(40, 50, "RESUMING")
    # wait(2000)
    base_motor.stop()
    elbow_motor.stop()
    gripper_motor.stop()
    ev3.screen.clear()

# this function is used for the comminucation between the two robots.
def coms(mbox):
    # global mbox
    mbox = Connect()
    while True:
        if thread2Alive[0] == False: break

        try:
            mbox.wait()
        except:
            wait(500)

        # Reads the message from robot, one of possible 6 messages from messages[].
        inbox = mbox.read()
        print(inbox)

        if inbox == messages[0]: # Occupied
            distributelist[1] = True # Collision warning!
            # distribute[0] = False # receevied is false.
            ev3.speaker.beep()
            ev3.screen.print("Collision warning!")
        # Package delivered (giftForme)
        elif inbox == messages[1]:
            ev3.speaker.beep()
            # Will go there and pick up the stuff
            # send[0] = 'occupied' # Send occupied signal.

            # Package has been delivered to us and safe to go there.
            distributelist[0] = True  # receevied
            # distribute[1] = False # occupied 
            wait(10)
            ev3.screen.print(inbox)
        # Free
        elif inbox == messages[5]:
            distributelist[0] = False # Occupied
            # distribute[1] = False # Receevied

        # Emergency stop
        elif inbox == messages[4]: # Emergency stop
            Em_stop[0] = True  # does this work? Idk


# this function is used to send messages between the connected robots.
def sendMessage(mbox):
    # global mbox
    print("sending message: ", send[0])
    ms = True

    while ms:
        try:
            if send[0] == messages[0]: # Occupied
                text = send[0]  # occupied
                mbox.send(text)
                ms = False
            elif send[0] == messages[1]: # gif4u
                text = send[0]  # gif4u
                mbox.send(text)
                ms = False
            elif send[0] == messages[2]: #'feed':
                text = send[0] #messages[2]  # feed
                print("sent message ", send[0])
                mbox.send(text)
                ms = False
            elif send[0] == messages[3]: # Stop belt
                text = send[0]  # stop
                mbox.send(text)
                ms = False
            elif send[0] == messages[4]: # Emergency
                text = send[0]  # emergency
                mbox.send(text)
                ms = False
        except:
            wait(5)
    if send[0] != messages[0]: # do not reset from occupied
        send[0] = messages[-1] # Set to nothing, we have sent the message.


# this function is used to connect the two robots together and identify which robot is the server and which one is the client.
def Connect():

    if me[0] == 'server':
        print("I'm server")
        server = BluetoothMailboxServer()
        me[0] = server
        ev3.screen.print("wait for connection")
        me[0].wait_for_connection()
        ev3.screen.clear()
        ev3.screen.print("Connected")
        wait(1000)
        ev3.screen.clear()
    else:
        # This is the name of the remote EV3 or PC we are connecting to.
        # SERVER = 'ev3dev'
        print("I'm Client")
        client = BluetoothMailboxClient()
        me[0] = client    
        me[0].connect(SERVERID)

        print('connected!')
        # client = BluetoothMailboxClient()
        ev3.speaker.beep()
    
    mbox = TextMailbox('greeting', me[0])

    return mbox


# this function is used to sort the items based on their colours.
def sorting_zones(pickup_zone, color_func):
    robot_pick(pickup_zone)
    if color_func() == "Red":
        if "Red" in active_zones:
            robot_release(active_zones["Red"])
            robot_pick(pickup_zone)
        else:
            robot_release(TRASH)
            robot_pick(pickup_zone)
    elif color_func() == "Blue":
        if "Blue" in active_zones:
            robot_release(active_zones["Blue"])
            robot_pick(pickup_zone)
        else:
            robot_release(TRASH)
            robot_pick(pickup_zone)
    elif color_func() == "Yellow":
        if "Yellow" in active_zones:
            robot_release(active_zones["Yellow"])
            robot_pick(pickup_zone)
        else:
            robot_release(TRASH)
            robot_pick(pickup_zone)
    elif color_func() == "Green":
        if "Green" in active_zones:
            robot_release(active_zones["Green"])
            robot_pick(pickup_zone)
        else:
            robot_release(TRASH)
            robot_pick(pickup_zone)
    else:
        robot_release(TRASH)
        robot_pick(pickup_zone)
#-------------------------------FUNCTION DEFINITIONS---------------------------------#

# ----------------------------------Variables & dictionaries---------------------------------#
# Time definitions
day, hour, minute, seconds = time_definitions()

###################### LEFT ##########################
# Left dominant paper 
LEFT_LEFT=210
LEFT=165
MIDDLE=115
RIGHT=15
TRASH=60

# Dictionary to store the release positions for each colour. LEFT
zone_dict = {
    1 : LEFT_LEFT,
    2 : LEFT,
    3 : MIDDLE,
    4 : RIGHT,
}
###################### LEFT ##########################

###################### RIGHT ##########################
# Right dominant paper
# LEFT_LEFT=210
# MIDDLE=115
# RIGHT = 60
# RIGHT_RIGHT=15
# TRASH = 165

# zone_dict = {
#     1 : LEFT_LEFT,
#     2 : MIDDLE,
#     3 : RIGHT,
#     4 : RIGHT_RIGHT,
# }
###################### RIGHT ##########################


# Dictionary with index keys to match with index keys from zone_dict below.
color_dict = {
    1 : "Red",
    2 : "Blue",
    3 : "Yellow",
    4 : "Green"
    }

if_count, sec_sched, pre_sec, menu_press_count = 0, 0, 0, 0
zone_picker, p = 1, 1
time_set, time_set_day, time_set_hour, time_set_min = False, False, False, False
day_set, hour_set, min_set = day, hour, minute
menu, center, check, pickup_zone, zones, conveyor_belt = True, False, False, False, False, False
communication, Done = False, False

# Main loop. The main program starts here.
while True:
# -------------------connection---------------------
    while Done == False:
        ev3.screen.draw_text(0, 0, "Pair with ")
        ev3.screen.draw_text(0, 20, "collaborator ?")
        ev3.screen.draw_text(0, 40, "Press center if YES")
        ev3.screen.draw_text(0, 70, "Press right if NO")
        if Button.CENTER in ev3.buttons.pressed():
            communication = True
            mbox = Connect()
            coms(mbox)
            ev3.screen.clear()
            ev3.screen.draw_text(50, 50, "Connected")
            print("Connected")
            wait(1000)
            ev3.screen.clear() 

            # if me[0] == 'server':
            #     me[0].send('')
            # elif me[0] == 'client':
            #     send[0] = 'feed'
            #     sendMessage(mbox)
            # wait(200)
            Done = True
        elif Button.RIGHT in ev3.buttons.pressed():
            communication = False
            Done = True
# -------------------connection--------------------------

# ----------------Pause and Resume button----------------
    # while emergency == False:   
    #     if Button.LEFT in ev3.buttons.pressed():
    #         emergency = True
    #         robot_pause()
    #         while emergency == True:
    #             if Button.RIGHT in ev3.buttons.pressed():
    #                 emergency = False
    #                 robot_resume()
    #                 continue
#-----------------Dashboard MENU-------------------------
    while menu == True:
        if menu_press_count < 0:
            menu_press_count = 0
        elif menu_press_count > 3:
            menu_press_count = -1

        if Button.DOWN in ev3.buttons.pressed():
            menu_press_count += 1
        elif Button.UP in ev3.buttons.pressed():
            menu_press_count += -1

        if menu_press_count == 0:  # Working Hours
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "--> Working Hours", Color.WHITE, Color.BLACK)
            ev3.screen.draw_text(0, 40, "Sorting Zones")
            ev3.screen.draw_text(0, 60, "Conveyor Belt")
            ev3.screen.draw_text(50, 80, "Start")
            wait(200)
            if Button.CENTER in ev3.buttons.pressed():
                ev3.screen.clear()
                center = True
                p = 0
                time_set_day = False
                time_set_hour = False
                time_set_min = False
            while center == True:
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "WORKING HOURS", Color.WHITE, Color.BLACK)
                ev3.screen.draw_text(0, 20, "Day: ")
                ev3.screen.draw_text(40, 20, day_set)
                ev3.screen.draw_text(0, 40, "Hour: ")
                ev3.screen.draw_text(60, 40, hour_set)
                ev3.screen.draw_text(0, 60, "Minute: ")
                ev3.screen.draw_text(80, 60, min_set)
                wait(200)

                while time_set_day == False:
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 0, "WORKING HOURS")
                    ev3.screen.draw_text(0, 20, "Day: ")
                    ev3.screen.draw_text(40, 20, day_set, Color.WHITE, Color.BLACK)
                    ev3.screen.draw_text(0, 40, "Hour: ")
                    ev3.screen.draw_text(60, 40, hour_set)
                    ev3.screen.draw_text(0, 60, "Minute: ")
                    ev3.screen.draw_text(80, 60, min_set)
                    wait(200)

                    if Button.UP in ev3.buttons.pressed():
                        ev3.screen.clear()
                        day_set += 1
                        if day_set > 31:
                            day_set = 31
                        elif day_set < day:
                            day_set = day
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        check = True
                    elif Button.DOWN in ev3.buttons.pressed():
                        ev3.screen.clear()
                        day_set -= 1
                        if day_set > 31:
                            day_set = 31
                        elif day_set < day:
                            day_set = day
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        check = True
                    elif Button.CENTER in ev3.buttons.pressed():
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        time_set_day = True
                    
                while time_set_hour == False:
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 0, "WORKING HOURS")
                    ev3.screen.draw_text(0, 20, "Day: ")
                    ev3.screen.draw_text(40, 20, day_set )
                    ev3.screen.draw_text(0, 40, "Hour: ")
                    ev3.screen.draw_text(60, 40, hour_set, Color.WHITE, Color.BLACK)
                    ev3.screen.draw_text(0, 60, "Minute: ")
                    ev3.screen.draw_text(80, 60, min_set)
                    wait(200)

                    if Button.UP in ev3.buttons.pressed():
                        ev3.screen.clear()
                        hour_set += 1
                        if hour_set < hour:
                            hour_set = hour
                            # day_set + day - 1
                        elif hour_set > 24:
                            hour_set = hour
                            # day_set + day + 1
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        check = True
                    elif Button.DOWN in ev3.buttons.pressed():
                        ev3.screen.clear()
                        hour_set -= 1
                        if hour_set < hour:
                            hour_set = hour
                            # day_set + day - 1
                        elif hour_set > 24:
                            hour_set = hour
                            # day_set + day + 1
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        check = True
                    elif Button.CENTER in ev3.buttons.pressed():
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set, Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set)
                        wait(200)
                        time_set_hour = True

                while time_set_min == False:
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 0, "WORKING HOURS")
                    ev3.screen.draw_text(0, 20, "Day: ")
                    ev3.screen.draw_text(40, 20, day_set)
                    ev3.screen.draw_text(0, 40, "Hour: ")
                    ev3.screen.draw_text(60, 40, hour_set)
                    ev3.screen.draw_text(0, 60, "Minute: ")
                    ev3.screen.draw_text(80, 60, min_set, Color.WHITE, Color.BLACK)
                    wait(200)

                    if Button.UP in ev3.buttons.pressed():
                        ev3.screen.clear()
                        min_set += 1
                        if min_set < minute:
                            min_set = minute
                            # day_set + day - 1
                        elif min_set > 59:
                            min_set = minute
                            # day_set + day + 1
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set, Color.WHITE, Color.BLACK)
                        wait(200)
                        check = True
                    elif Button.DOWN in ev3.buttons.pressed():
                        ev3.screen.clear()
                        min_set -= 1
                        if min_set < minute:
                            min_set = minute
                            # day_set + day - 1
                        elif min_set > 59:
                            min_set = minute
                            # day_set + day + 1
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set, Color.WHITE, Color.BLACK)
                        wait(200)
                        check = True
                    elif Button.CENTER in ev3.buttons.pressed():
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 0, "WORKING HOURS")
                        ev3.screen.draw_text(0, 20, "Day: ")
                        ev3.screen.draw_text(40, 20, day_set)
                        ev3.screen.draw_text(0, 40, "Hour: ")
                        ev3.screen.draw_text(60, 40, hour_set)
                        ev3.screen.draw_text(0, 60, "Minute: ")
                        ev3.screen.draw_text(80, 60, min_set, Color.WHITE, Color.BLACK)
                        wait(200)
                        time_set_min = True

                if Button.LEFT in ev3.buttons.pressed():
                    # Converts given time to seconds
                    sec_sched = day_set*86400 + hour_set*3600 + min_set*60
                    center = False
                    ev3.screen.clear()
        elif menu_press_count == 1: # Sorting Zones
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "Working Hours")
            ev3.screen.draw_text(0, 40, "--> Sorting Zones", Color.WHITE, Color.BLACK)
            ev3.screen.draw_text(0, 60, "Conveyor Belt")
            ev3.screen.draw_text(50, 80, "Start")
            wait(200)
            if Button.CENTER in ev3.buttons.pressed():
                ev3.screen.clear()
                wait(300)
                center = True
                pickup_zone = False
                zones = False
                zone_picker = 1
                p = 0

            while center == True:
                ev3.screen.clear()

                while pickup_zone == False:
                    print(p)
                    if p < 1:
                        p = 1
                    elif p > 4:
                        p = 4
                    ev3.screen.draw_text(50, 0, "Pick-Up Zone (CENTER=DONE)")
                    if Button.UP in ev3.buttons.pressed():
                        wait(300)
                        ev3.screen.clear()
                        p += 1
                        if p < 1:
                            p = 1
                        elif p > 4:
                            p = 4
                        ev3.screen.draw_text(50, 0, "Pick-Up Zone (CENTER=DONE)")
                        ev3.screen.draw_text(0, 40, p)
                        check = True
                    elif Button.DOWN in ev3.buttons.pressed():
                        wait(300)
                        ev3.screen.clear()
                        p -= 1
                        if p < 1:
                            p = 1
                        elif p > 4:
                            p = 4
                        ev3.screen.draw_text(50, 0, "Pick Up Zone (CENTER=DONE)")
                        ev3.screen.draw_text(0, 40, p)
                        check = True
                    elif Button.CENTER in ev3.buttons.pressed():
                        wait(300)
                        ev3.screen.clear()
                        if p < 1:
                            p = 1
                        elif p > 4:
                            p = 4
                        print(p)
                        print(zone_dict[p])
                        active_zones.update({'Pick-Up Zone' : zone_dict[p]})
                        print(active_zones['Pick-Up Zone'])
                        p = 1
                        if check == True:
                            pickup_zone = True

                if pickup_zone == True and if_count == 0:
                    p = 1
                    ev3.screen.draw_text(0, 40, "Pick-Up Zone SET")
                    wait(1000)
                    ev3.screen.clear()
                    if_count += 1

                while zones == False:
                    if zone_picker >= 3:
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 40, zones)
                        zones = True
                        ev3.screen.draw_text(0, 80, zones)
                    else:
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 40, "Sorting Zones")

                    if p < 1:
                        p = 1
                    elif p > 4:
                        p = 4
                        
                    while zone_picker < 5:
                        if p < 1:
                            p = 1
                        elif p > 4:
                            p = 4

                        if active_zones['Pick-Up Zone'] == zone_dict[zone_picker]:
                            ev3.screen.clear()
                            zone_picker += 1
                            ev3.screen.draw_text(0, 40, "Pick-Up Zone")
                            wait(300)
                        
                        if Button.UP in ev3.buttons.pressed():
                            p += 1
                            ev3.screen.clear()
                            ev3.screen.draw_text(0, 0, "Zone: ")
                            ev3.screen.draw_text(50, 20, zone_picker)
                            wait(300)                                

                            if p < 1:
                                p = 1
                            elif p > 4:
                                p = 4

                            if color_dict[p] == 'Taken' and p < 4:
                                p += 1
                            if color_dict[4] == 'Taken' and color_dict[3] == 'Taken':
                                p = 2
                            if color_dict[4] == 'Taken' and color_dict[3] == 'Taken' and color_dict[2] == 'Taken':
                                p = 1
                            if color_dict[p] == 'Taken' and p == 4:
                                p = 3
                            if p < 1:
                                p = 1
                            elif p > 4:
                                p = 4

                            ev3.screen.draw_text(0, 40, color_dict[p])
                            pickup_col = color_dict[p]

                        elif Button.DOWN in ev3.buttons.pressed():
                            p -= 1
                            ev3.screen.clear()
                            ev3.screen.draw_text(0, 0, "Zone: ")
                            ev3.screen.draw_text(50, 20, zone_picker)
                            wait(300)
                            
                            if p < 1:
                                p = 1
                            elif p > 4:
                                p = 4

                            if color_dict[p] == 'Taken' and p > 1:
                                p -= 1
                            if color_dict[1] == 'Taken' and color_dict[2] == 'Taken':
                                p = 3
                            if color_dict[1] == 'Taken' and color_dict[2] == 'Taken' and color_dict[3] == 'Taken':
                                p = 4
                            if color_dict[p] == 'Taken' and p == 1:
                                p = 2

                            if p < 1:
                                p = 1
                            elif p > 4:
                                p = 4
                            
                            ev3.screen.draw_text(0, 40, color_dict[p])
                            pickup_col = color_dict[p]
                        elif Button.CENTER in ev3.buttons.pressed():
                            ev3.screen.clear()
                            ev3.screen.draw_text(0, 0, "Zone: ")
                            ev3.screen.draw_text(0, 20, zone_picker)
                            ev3.screen.draw_text(0, 40, "set to: ")
                            if p < 1:
                                p = 1
                            elif p > 4:
                                p = 4

                            ev3.screen.draw_text(0, 60, color_dict[p])
                            
                            active_zones.update({color_dict[p] : zone_dict[zone_picker]})
                            color_dict.update({p : 'Taken'})

                            for key in active_zones:
                                if active_zones[key] == 'Taken':
                                    active_zones.pop(key, 'Taken')

                                    ev3.screen.clear()
                                    ev3.screen.draw_text(0, 60, "Choose Color")
                            wait(400)      
                            zone_picker += 1
                
                for key in active_zones:
                    print(key)
                    print(active_zones[key])

                center = False
        elif menu_press_count == 2: # With or Without Conveyor belt
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "Working Hours")
            ev3.screen.draw_text(0, 40, "Sorting Zones")
            ev3.screen.draw_text(0, 60, "--> Conveyor Belt", Color.WHITE, Color.BLACK)
            ev3.screen.draw_text(50, 80, "Start")
            wait(200)
            if Button.CENTER in ev3.buttons.pressed(): # And rest have been chosen
                wait(200)
                ev3.screen.clear()
                p=1
                while conveyor_belt == False:
                    while p == 1:
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 0, "Conveyor Belt")
                        ev3.screen.draw_text(50, 20, "Yes", Color.WHITE, Color.BLACK)
                        ev3.screen.draw_text(50, 40, "No")
                        if Button.DOWN in ev3.buttons.pressed():
                            p += 1
                        wait(200)
                        if Button.CENTER in ev3.buttons.pressed():
                            conveyor_belt = True
                            belt = True
                            break
                    while p == 2:
                        ev3.screen.clear()
                        ev3.screen.draw_text(0, 0, "Conveyor Belt")
                        ev3.screen.draw_text(50, 20, "Yes")
                        ev3.screen.draw_text(50, 40, "No", Color.WHITE, Color.BLACK)
                        if Button.UP in ev3.buttons.pressed():
                            p -= 1
                        wait(200)
                        if Button.CENTER in ev3.buttons.pressed():
                            conveyor_belt = True
                            belt = False
                            break
        elif menu_press_count == 3: # Start
            ev3.screen.clear()
            ev3.screen.draw_text(50, 0, "MENU")
            ev3.screen.draw_text(0, 20, "Working Hours")
            ev3.screen.draw_text(0, 40, "Sorting Zones")
            ev3.screen.draw_text(0, 60, "Conveyor Belt")
            ev3.screen.draw_text(50, 80, "--> Start", Color.WHITE, Color.BLACK)
            wait(200)
            if Button.CENTER in ev3.buttons.pressed(): # And rest have been chosen
                ev3.screen.clear()
                menu = False

    # ticker(sec_sched)
    # Timer 
    while sec_sched > pre_sec:
        day, hour, minute, seconds = time_definitions()
        pre_sec = day*86400 + hour*3600 + minute*60 + seconds

        ev3.screen.draw_text(10, 50, "Waiting to Start", Color.WHITE, Color.BLACK)
        ev3.screen.draw_text(65, 70, sec_sched - pre_sec, Color.WHITE, Color.BLACK)
#-----------------DASHBOARD MENU-------------------------
   
    # If robot connect
    if belt == True and communication == False:
        server = BluetoothMailboxServer()
        mbox = TextMailbox('greeting', server)
        
        print('waiting for connection...')
        server.wait_for_connection()
        print('connected!')

        # Resets the arm's elbow position. Touches the bottom.
        elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=10)
        print(elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=10))

        # Close gripper if not closed
        gripper_motor.run_until_stalled(100, then=Stop.COAST, duty_limit=50)

        # Resets elbow_motor angle to zero so we can use it later.
        elbow_motor.reset_angle(0)
        print(elbow_motor.angle())
        elbow_motor.hold()

        # Moves up 80 degrees.
        elbow_motor.run_angle(100, 80, then=Stop.HOLD)

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
        gripper_motor.run_until_stalled(100, then=Stop.HOLD, duty_limit=25)
        gripper_motor.reset_angle(0)
        gripper_motor.run_target(150, -90)
    elif belt == False and communication == True:
        while communication == True and belt == False:
            sendMessage(mbox)
            coms(mbox)
            print(sendMessage(mbox))
            print(coms(mbox))
            print(mbox)
            if distributelist[0] == True and distributelist[1] == False:
                # Delivered
                elbow_motor.stop()
                base_motor.stop()
                gripper_motor.stop()
            elif distributelist[0] == False and distributelist[1] == False:
                # Free
                # sorting_zones(active_zones['Pick-Up Zone'], color_func())
                robot_pick(active_zones['Pick-Up Zone'])
                if color_func() == "Red":
                    if "Red" in active_zones:
                        robot_release(active_zones["Red"])
                        robot_pick(active_zones['Pick-Up Zone'])
                    else:
                        robot_release(TRASH)
                        robot_pick(active_zones['Pick-Up Zone'])
                elif color_func() == "Blue":
                    if "Blue" in active_zones:
                        robot_release(active_zones["Blue"])
                        robot_pick(active_zones['Pick-Up Zone'])
                    else:
                        robot_release(TRASH)
                        robot_pick(active_zones['Pick-Up Zone'])
                elif color_func() == "Yellow":
                    if "Yellow" in active_zones:
                        robot_release(active_zones["Yellow"])
                        robot_pick(active_zones['Pick-Up Zone'])
                    else:
                        robot_release(TRASH)
                        robot_pick(active_zones['Pick-Up Zone'])
                elif color_func() == "Green":
                    if "Green" in active_zones:
                        robot_release(active_zones["Green"])
                        robot_pick(active_zones['Pick-Up Zone'])
                    else:
                        robot_release(TRASH)
                        robot_pick(active_zones['Pick-Up Zone'])
                else:
                    robot_release(TRASH)
                    robot_pick(active_zones['Pick-Up Zone'])
            elif distributelist[0] == False and distributelist[1] == True:
                # Collision Warning
                elbow_motor.stop()
                base_motor.stop()
                gripper_motor.stop()
    else:
        # Resets the arm's elbow position. Touches the bottom.
        elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=10)
        print(elbow_motor.run_until_stalled(-40, then=Stop.HOLD, duty_limit=10))

        # Close gripper if not closed
        gripper_motor.run_until_stalled(100, then=Stop.COAST, duty_limit=50)

        # Resets elbow_motor angle to zero so we can use it later.
        elbow_motor.reset_angle(0)
        print(elbow_motor.angle())
        elbow_motor.hold()

        # Moves up 80 degrees.
        elbow_motor.run_angle(100, 80, then=Stop.HOLD)

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
        gripper_motor.run_until_stalled(100, then=Stop.HOLD, duty_limit=25)
        gripper_motor.reset_angle(0)
        gripper_motor.run_target(150, -90)

    ev3.screen.clear()

    # while color_func() != None:
    while belt == True:
        # What's left with conveyor belt
        # Being able to pick if you wanna go with conveyor belt or not (variable belt)
        # Make it more smooth
        if color_func() != None:
            base_motor.run_target(300, active_zones["Pick-Up Zone"])
            elbow_motor.stop()
            if color_func() == "Red":
                if "Red" in active_zones:
                    mbox.send('Wait!')
                    robot_pick(active_zones['Pick-Up Zone'])
                    robot_release(active_zones["Red"])
                    mbox.send('Go')
                else:
                    robot_release(TRASH)
                    robot_pick(active_zones['Pick-Up Zone'])
            elif color_func() == "Blue":
                if "Blue" in active_zones:
                    mbox.send('Wait!')
                    robot_pick(active_zones['Pick-Up Zone'])
                    robot_release(active_zones["Blue"])
                    mbox.send('Go')
                else:
                    robot_release(TRASH)
                    robot_pick(active_zones['Pick-Up Zone'])
            elif color_func() == "Yellow":
                if "Yellow" in active_zones:
                    mbox.send('Wait!')
                    robot_pick(active_zones['Pick-Up Zone'])
                    robot_release(active_zones["Yellow"])
                    mbox.send('Go')
                else:
                    robot_release(TRASH)
                    robot_pick(active_zones['Pick-Up Zone'])
            elif color_func() == "Green":
                if "Green" in active_zones:
                    mbox.send('Wait!')
                    robot_pick(active_zones['Pick-Up Zone'])
                    robot_release(active_zones["Green"])
                    mbox.send('Go')
                else:
                    robot_release(TRASH)
                    robot_pick(active_zones['Pick-Up Zone'])
    while belt == False:
        robot_pick(active_zones['Pick-Up Zone'])
        if color_func() == "Red":
            if "Red" in active_zones:
                robot_release(active_zones["Red"])
                robot_pick(active_zones['Pick-Up Zone'])
            else:
                robot_release(TRASH)
                robot_pick(active_zones['Pick-Up Zone'])
        elif color_func() == "Blue":
            if "Blue" in active_zones:
                robot_release(active_zones["Blue"])
                robot_pick(active_zones['Pick-Up Zone'])
            else:
                robot_release(TRASH)
                robot_pick(active_zones['Pick-Up Zone'])
        elif color_func() == "Yellow":
            if "Yellow" in active_zones:
                robot_release(active_zones["Yellow"])
                robot_pick(active_zones['Pick-Up Zone'])
            else:
                robot_release(TRASH)
                robot_pick(active_zones['Pick-Up Zone'])
        elif color_func() == "Green":
            if "Green" in active_zones:
                robot_release(active_zones["Green"])
                robot_pick(active_zones['Pick-Up Zone'])
            else:
                robot_release(TRASH)
                robot_pick(active_zones['Pick-Up Zone'])
        else:
            robot_release(TRASH)
            robot_pick(active_zones['Pick-Up Zone'])

# to be continued...

