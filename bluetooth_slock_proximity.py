#!/usr/bin/env python

import bluetooth
import sys
import os
import time
import subprocess
import re
import sqlite3
from sqlite3 import Error
from datetime import datetime

PORT = 3  # bluetooth port
ADDR = 'CC:21:19:CF:F9:F2'  # device bluetooth address - CHANGE THIS
LOCKER = 'slock'  # system locker - CHANGE THIS


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
        return conn
    except Error as e:
        print(e)


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


def send_notification(title, body):
    """
    sends notification using pushbullet
    """
    ps = subprocess.Popen(['/home/vicente/.i3/pushbullet/notify.sh', '-t', title, '-b', body], stdout=subprocess.PIPE)

    return


conn = create_connection("bluetooth.db")
conn.close()

try:
    if not connection_check():
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((ADDR, PORT))
except bluetooth.btcommon.BluetoothError as err:
    pass

if connection_check():
    prox = proximity_check()
    if prox < -5:
        print('  ')
        send_message('Too far away. Locking device..')
        time.sleep(4)
        ps = subprocess.Popen(['pgrep', LOCKER], stdout=subprocess.PIPE)
        ps = ps.communicate()[0].decode('utf-8')
        if not ps:  # if locker has already been invoked, so it doesn't invoke infinite lockers
            send_notification('LOCKED', 'Too far away ' + str(prox))
            time.sleep(1)  # without it notification would only arrive after unlock
            ps = subprocess.Popen([LOCKER], stdout=subprocess.PIPE)
    else:
        print('  ')
else:
    send_message('Not connected.. Locking device..')
    time.sleep(4)
    ps = subprocess.Popen(['pgrep', LOCKER], stdout=subprocess.PIPE)
    ps = ps.communicate()[0].decode('utf-8')
    if not ps:  # check if locker has already been invoked, so it doesn't invoke infinite lockers
        if not connection_check():
            print('  ')
            send_notification('LOCKED', 'No connection')
            time.sleep(1)  # hammered fix - without it notification would only arrive after unlock
            ps = subprocess.Popen([LOCKER], stdout=subprocess.PIPE)
        else:
            send_notification('LOCKED CANCELLED', 'Connected')
            print('  ')

