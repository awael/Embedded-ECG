import serial
import time
import struct
import os

ser = serial.Serial('COM4',baudrate = 115200, timeout=1)
samplingRate = input("please enter sampling rate: ")
time.sleep(2)
ser.write(struct.pack('>B', int(samplingRate)))
timeout = time.time() + 60
while True:
    data = ser.readline()
    os.write(1, data)
    #print(data)
    if time.time() > timeout:
        break
ser.close()
