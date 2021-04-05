import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
from scipy.io.wavfile import write


def num2dac(va):
    x = []
    for i in range(8):
        if va % 2 == 1:
            x.append(1)
            va = (va - 1) / 2
        else:
            x.append(0)
            va = va / 2
    return x


def first():
    while True:
        for i in range(8):
            GPIO.output(ind[i], 0)
        print("Введите число (-1 для выхода):")
        value = input()
        try:
            value = int(value)
        except ValueError:
            exit()
        if value > 255 or value < 0:
            exit()
        x = num2dac(value)
        for i in range(8):
            GPIO.output(ind[i], x[i])
        time.sleep(1)


def second():
    rep = input()
    try:
        rep = int(rep)
    except ValueError:
        exit()
    if rep < 0:
        exit()
    for _ in range(rep):
        for i in range(256):
            x = num2dac(i)
            for j in range(8):
                GPIO.output(ind[j], x[j])
            time.sleep(0.01)
        for i in range(255, -1, -1):
            x = num2dac(i)
            for j in range(8):
                GPIO.output(ind[j], x[j])
            time.sleep(0.01)


def third():
    ti = input()
    fr = input()
    sfr = input()
    try:
        ti = float(ti)
        fr = float(fr)
        sfr = float(sfr)
    except ValueError:
        exit()
    t = np.arange(0, ti, 1/sfr)
    amp = np.sin(fr/3.14*t)
    for i in range(len(t)):
        amp[i] = int(254 / 2 * (1 + amp[i]) + 1)
    plt.plot(t, amp)
    plt.title('Синус')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда sin(time)')
    plt.show()
    for i in range(len(t)):
        x = num2dac(amp[i])
        for j in range(8):
            GPIO.output(ind[j], x[j])
        time.sleep(1/sfr)


def fourth():
    data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
    wav_fname = pjoin(data_dir, 'SOUND.WAV')
    sfr, data = wavfile.read(wav_fname)
    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sfr
    print(f"length = {length}s")
    for i in data[:, 0]:
        x = num2dac(i)
        for j in range(8):
            GPIO.output(ind[j], x[j])
        time.sleep(1/sfr)


GPIO.setmode(GPIO.BCM)
ind = [10, 9, 11, 5, 6, 13, 19, 26]
GPIO.setup(ind, GPIO.OUT)
try:
    third()
finally:
    for i in range(8):
        GPIO.output(ind[i], 0)
