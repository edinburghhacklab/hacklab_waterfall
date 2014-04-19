#!/usr/bin/env python

from PIL import Image
import serial
import struct
import sys
import time

device = sys.argv[1]
filename = sys.argv[2]
delay = float(sys.argv[3])

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
    ser.write(chr(len(bytes)) + struct.pack('%sB' % len(bytes), *bytes))
    ser.flush()

def main():
    bytes = [0]*8

    for y in range(im.size[1]):
        for i in range(8):
            bytes[i] = 0
            for x in range(8):
                bytes[i] <<= 1;
                bytes[i] |= (im.getpixel((x + i*8, y)) == 0)
                #if byte & 1:
                #    sys.stdout.write('#')
                #else:
                #    sys.stdout.write(' ')
        if ser:
            send_bytes(bytes)
        else:
            print_bytes(bytes)
        time.sleep(delay)
	
if device != "":
    ser = serial.Serial(device, baudrate=115200)
else:
    ser = None

im = Image.open(filename)
(width, height) = im.size
new_width = 64
new_height = int(float(new_width)/float(width) * float(height))
im = im.convert("1", dither=Image.NONE)
im = im.resize((new_width, new_height))
im = im.transpose(Image.FLIP_TOP_BOTTOM)
#im.draft('1', (new_width, new_height))
#im.show()

while True:
    main()
    