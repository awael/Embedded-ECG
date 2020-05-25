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
    i = i + 1
    xs.append(i)
    if x[0] == '' or x[0] == "\n" or int(x[0]) > 4096 or int(x[0]) < 0:
        x[0] = 0
    if len(x) < 2:
        x.append("0\n")
    if x[1] == '' or x[1] == "\n":
        x[1] = "0\n"

    ys.append(int(x[0]))
    if (i > 100):  # window size
        del xs[0];
        del ys[0];

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('BPM = ' + str(round(int(x[1][:-1]) / ((time.time() - tic) / 60))))
    plt.ylabel('Amplitude')
    if time.time() - tic > 58:
        ani.event_source.stop()
        if argv[2] != 'hold':
            plt.close()


ser = serial.Serial(third, baudrate=int(fourth), timeout=None)
time.sleep(1)
ser.write(struct.pack('>B', int(first)))
time.sleep(1)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
fig.subplots_adjust(top=0.85)

xs = []
ys = []
i = 0
time.sleep(1)
myText = ax.text(0.1, 0.1, 'BPM')
counter = 0
tic = time.time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=0.01, save_count=100, blit=False)
time.sleep(1)
plt.show()
ser.close()
