#!/usr/bin/env python

from PIL import Image
import serial
import struct
import sys
import time

device = sys.argv[1]
#ser = serial.Serial(device, baudrate=115200)
delay = float(sys.argv[2])
filename = sys.argv[3]

def print_bytes(bytes):
    for a in range(0, len(bytes)):
        for b in range(7, -1, -1):
            if bytes[a] & (1<<b):
                sys.stdout.write(" X")
            else:
                sys.stdout.write("  ")
    sys.stdout.write("\n")
    sys.stdout.flush()

def send_bytes(bytes):
    ser.write(chr(len(bytes)), struct.pack('%sB' % len(bytes), *bytes))
    ser.flush()

im = Image.open(filename)
im.draft('1', (64, 64))
#im.show()
bytes = [0]*8

for y in range(64):
	for i in range(8):
		bytes[i] = 0
		for x in range(8):
			bytes[i] <<= 1;
			bytes[i] |= (im.getpixel((x + i*8, y)) == 0)
			#if byte & 1:
			#	sys.stdout.write('#')
			#else:
			#	sys.stdout.write(' ')
	print_bytes(bytes)
	time.sleep(delay)
	