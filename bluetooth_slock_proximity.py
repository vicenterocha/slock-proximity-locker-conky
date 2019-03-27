#!/usr/bin/env python

import bluetooth
import sys
import os
import time
import subprocess
import re

PORT = 3  # bluetooth port
ADDR = 'CC:21:19:CF:F9:F2'  # device bluetooth address - CHANGE THIS
LOCKER = 'slock'  # system locker - CHANGE THIS


def send_message(message):
    """
    sends system notification
    """
    subprocess.Popen(['notify-send', message])
    return


def connection_check():
    """
    checks if device is connected. Returns True if connected, else False
    """
    ps = subprocess.Popen(['hcitool', 'con'], stdout=subprocess.PIPE)
    device = ps.communicate()[0].decode('utf-8')

    if ADDR in device:
        return True
    else:
        return False


def proximity_check():
    """
    checks if device is nearby, returns rssi value
    """
    ps = subprocess.Popen(['hcitool', 'rssi', ADDR], stdout=subprocess.PIPE)
    proximity = ps.communicate()
    if proximity[0]:
        proximity = proximity[0].decode('utf-8')
    else:
        return -1
    proximity = [int(d) for d in re.findall(r'-?\d+', proximity)]

    return proximity[0]


# while True:
# blindly tries to connect everytime (TODO smooth)
try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((ADDR, PORT))
except bluetooth.btcommon.BluetoothError as err:
    pass

if connection_check():
    print('  ')
    if proximity_check() < 0:
        print('  ')
        send_message('Too far away. Locking device..')
        time.sleep(5)
        ps = subprocess.Popen(['pgrep', LOCKER], stdout=subprocess.PIPE)
        ps = ps.communicate()[0].decode('utf-8')
        if not ps:  # check if locker has already been invoked, so it doesn't invoke infinite lockers
            ps = subprocess.Popen([LOCKER], stdout=subprocess.PIPE)
else:
    send_message('Not connected.. Locking device..')
    print('  ')
    time.sleep(5)
    ps = subprocess.Popen(['pgrep', LOCKER], stdout=subprocess.PIPE)
    ps = ps.communicate()[0].decode('utf-8')
    if not ps:  # check if locker has already been invoked, so it doesn't invoke infinite lockers
        ps = subprocess.Popen([LOCKER], stdout=subprocess.PIPE)

# time.sleep(5)
