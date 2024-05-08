#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, BluetoothMailboxClient 
import time

# Initialize the EV3 Brick
ev3 = EV3Brick()

conveyor_motor = Motor(Port.D)

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3dev-D'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

while True:
    if mbox.read() == "Wait!":
        conveyor_motor.stop()
        print(mbox.read())
    elif mbox.read() == "Go":
        conveyor_motor.run(50)
    else:
        conveyor_motor.run(50)

# In this program, the client sends the first message and then waits for the
# server to reply.
# mbox.send('hello!')
# mbox.wait()
# print(mbox.read())