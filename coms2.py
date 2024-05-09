#!/usr/bin/env pybricks-micropython

# from Parameters import *

from pybricks import robotics
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.messaging import BluetoothMailboxClient, TextMailbox, BluetoothMailboxServer

# from pybricks.hubs import EV3Brick
# from pybricks.messaging import BluetoothMailboxClient, TextMailbox, BluetoothMailboxServer
# from pybricks.tools import wait, StopWatch



ev3 = EV3Brick()


collaborators = ['A', 'B', 'C', 'D', 'E','F', 'G']
RobotIdentity = 'A'
# collaborator = 'D'

# The server must be started before the client!
# me = ['server']
me = ['client']

 # This is the name of the remote EV3 or PC we are connecting to.
# SERVERID = 'ev3dev-' + collaborator

messages = ['occupied', 'gift4u', 'feed', 'stop', 'emergency', 'free', 'nothing']
# 0 send nothing, 1 for occupied, 2 for gift4u, 3 feed, 4 stop, 5 free.
send = ['nothing']

# Coms thread.
thread2Alive = [False]

# Make empty mbox for later!
mbox = ''

Estop = [False]




distributeText = ['receevied', 'deliver']  #0 : receevied, 1: deliver.
distribute = [False, False]




def coms(mbox):
    # global mbox
    # mbox = Connect()
    print("I'm listning")
    while True:
        if thread2Alive[0] == False: break

        try:
            mbox.wait()
        except:
            wait(500)

        inbox = mbox.read()

        print("Recevied message: ", str(inbox))

        if inbox == messages[0]: # Occupied
            distribute[1] = True # Collision warning!
            # Detta fel.
            # distribute[0] = False # receevied is false.
            ev3.speaker.beep()
            ev3.screen.print("Collision warning!")
        
        elif inbox == messages[1]: # giftForme
            ev3.speaker.beep()
            # Will go there and pick up the stuff
            # send[0] = 'occupied' # Send occupied signal.

            # Package has been delivered to us and safe to go there.
            distribute[0] = True  # receevied
            # Fel.
            # distribute[1] = False # occupied 
            wait(10)
            ev3.screen.print(inbox)
            # while True:
            #     if send[0] == 0:
            #         text = messages[0]
            #         print(text)
            #         sendMessage()
            #         # mbox.send(text)
            #         send[0] == 3
            #         break
            #     else:
            #         wait(300)
        elif inbox == messages[5]: # Free
            distribute[0] = False # Occupied
            # distribute[1] = False # Receevied
        elif inbox == messages[4]: # Emergency stop
            Estop[0] = True  # does this work?


        
        


def sendMessage(mbox):
    # global mbox
    print("sending message: ", send[0])
    do = True

    while do:
        try:
            if send[0] == messages[0]: # Occupied
                text = send[0]  # occupied
                mbox.send(text)
                do = False
            elif send[0] == messages[1]: # gif4u
                text = send[0]  # gif4u
                mbox.send(text)
                do = False
            elif send[0] == messages[2]: #'feed':
                text = send[0] #messages[2]  # feed
                print("sent message ", send[0])
                mbox.send(text)
                do = False
            elif send[0] == messages[3]: # Stop belt
                text = send[0]  # stop
                mbox.send(text)
                do = False
            elif send[0] == messages[4]: # Emergency
                text = send[0]  # emergency
                mbox.send(text)
                do = False
        except:
            wait(5)

    if send[0] != messages[0]: # do not reset from occupied
        send[0] = messages[-1] # Set to nothing, we have sent the message.






# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.
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
        mbox = TextMailbox('greeting', me[0])

    else:
        print("I'm Client")
        client = BluetoothMailboxClient()
        me[0] = client
        mbox = TextMailbox('greeting', me[0])
        for collaborator in collaborators:
                # This is the name of the remote EV3 or PC we are connecting to.
                SERVERID = 'ev3dev-' + collaborator
                ev3.screen.print("Attempting to connect to\n" + SERVERID)
                if collaborator != RobotIdentity:
                    try:
                        ev3.screen.print('establishing connection...')
                        wait(10)
                        me[0].connect(SERVERID)
                        ev3.screen.clear()
                        ev3.screen.print("Connected")
                        wait(1000)
                        ev3.screen.clear()
                    except ValueError:
                        ev3.screen.print("Failed to connect to\n"+ SERVERID)
                        wait(1000)
                        ev3.screen.clear()
        # client = BluetoothMailboxClient()
        # me[0] = client    
        # me[0].connect(SERVERID)
        # print('connected!')
        # client = BluetoothMailboxClient()
    

    
    return mbox




if __name__ == "__main__":
    mbox = Connect()
    coms(mbox)