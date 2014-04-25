#!/usr/bin/env python

import random
import serial
import struct
import sys
import time

device = sys.argv[1]
mode = sys.argv[2]
delay = float(sys.argv[3])

class Controller(object):
    def __init__(self, ser=None):
        self.ser = ser
        self.clear_all()
    def set(self, bit):
        self.bits[bit] = True
    def clear(self, bit):
        self.bits[bit] = False
    def set_all(self):
        self.bits = [True]*64
    def clear_all(self):
        self.bits = [False]*64
    def display(self):
        for i in range(0, len(self.bits)):
            if self.bits[i]:
                sys.stdout.write(" X")
            else:
                sys.stdout.write("  ")
        sys.stdout.write("\n")
        sys.stdout.flush()
    def get_byte(self, num):
        offset = num*8
        output = 0
        for i in range(0, 8):
            if self.bits[offset+i]:
                output += 1<<7-i
        return output
    def get_bytes(self):
        output = []
        for num in range(0, 8):
            output.append(self.get_byte(num))
        return output
    def send(self):
        if self.ser:
            ser.write(chr(8)+struct.pack('8B', *self.get_bytes()))
            ser.flush()
        else:
            self.display()

def sweep():
    for i in range(0, 64):
        controller.clear_all()
        controller.set(i)
        controller.send()
        time.sleep(delay)

def bounce():
    for i in range(0, 64):
        controller.clear_all()
        controller.set(i)
        controller.send()
        time.sleep(delay)
    for i in range(62, 0, -1):
        controller.clear_all()
        controller.set(i)
        controller.send()
        time.sleep(delay)
        
def rand():
    controller.clear_all()
    controller.set(random.randint(0, 63))
    controller.send()
    time.sleep(delay)

def pulse(on_count=1, off_count=1):
    controller.set_all()
    controller.send()
    for i in range(0, on_count):
        time.sleep(delay)
    controller.clear_all()
    controller.send()
    for i in range(0, off_count):
        time.sleep(delay)

def pulse2(on_count=1, off_count=1):
    controller.set_all()
    for i in range(0, 8) + range(16, 24) + range(32, 40) + range(48, 56):
        controller.clear(i)
    controller.send()
    for i in range(0, on_count):
        time.sleep(delay)

    controller.clear_all()
    for i in range(0, 8) + range(16, 24) + range(32, 40) + range(48, 56):
        controller.set(i)
    controller.send()
    for i in range(0, off_count):
        time.sleep(delay)

def multisweep():
    width = 20
    for i in range(0, 64 - width):
        controller.set_all()
        for j in range(i, i + width):
            controller.clear(j)
        controller.send()
        time.sleep(delay)

if device != "":
    ser = serial.Serial(device, baudrate=115200)
    controller = Controller(ser)
else:
    controller = Controller()

if mode == "sweep":
    fn = sweep
elif mode == "bounce":
    fn = bounce
elif mode == "pulse":
    fn = pulse
elif mode == "pulse2":
    fn = pulse2
elif mode == "multisweep":
    fn = multisweep
else:
    fn = rand
    
while True:
    fn()
