import serial
import time
import struct
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import getopt
from sys import argv

script, first, second, third, fourth = argv


def animate(i, xs, ys):
    # Aquire and parse data from serial port
    try:
        line = ser.readline().decode('utf-8')
    except ValueError:
        line = ser.readline().decode('utf-8')
    x = line.split(",")
    #print(line)
    i = i + 1
    # Add x and y to lists
    xs.append(i)
    if x[0] == '' or x[0] == "\n" or int(x[0]) > 4096 or int(x[0]) < 0:
        x[0] = 0
    if len(x) < 2:
        x.append("0\n")
    if x[1] == '' or x[1] == "\n":
        x[1] = "0\n"


    ys.append(int(x[0]))
    # os.write(1, line)
    # Limit x and y lists to 20 items
    # xs = xs[-900:]
    # ys = ys[-900:]
    if (i > 100):  # window size
        del xs[0];
        del ys[0];

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('BPM = '+str(round(int(x[1][:-1])/((time.time()-tic)/60))))
    plt.ylabel('Amplitude')
    if time.time()-tic > 59:
        ani.event_source.stop()
        if argv[2] != 'hold':
            plt.close()

    # plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
    # plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo


ser = serial.Serial(third, baudrate=int(fourth), timeout=None)
# samplingRate = input("please enter sampling rate in SPS: ")
t = int(first)
time.sleep(1)
ser.write(struct.pack('>B', int(int(first)/7)))
timeout = time.time() + 20  # changed to 20 for the demo
time.sleep(1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.subplots_adjust(top=0.85)

xs = []  # store trials here (n)
ys = []  # store relative frequency here
i = 0
time.sleep(1)
myText = ax.text(0.1, 0.1, 'BPM')
counter = 0
plt.ylim(0, 4096)
tic = time.time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=0.01, save_count=100, blit=False)
time.sleep(1)
plt.show()
ser.close()
