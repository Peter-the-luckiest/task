import numpy as np
import time
import RPi.GPIO as gp
import scipy.io.wavfile

pins = [10, 9, 11, 5, 6, 13, 19, 26]
gp.setmode(gp.BCM)
gp.setup(pins, gp.OUT)


def dec_to_bin(val):
    out = [0] * 8
    for i in range(7, -1, -1):
        if val // 2**i != 0:
            out[i] = 1
            val %= 2**i
    return out


def light(val):
    array = dec_to_bin(val)
    gp.output(pins, array)


def play(array, st):
    for val in array:
        light(val)
        time.sleep(0)



try:
    if __name__ == "__main__":
        sr, array = scipy.io.wavfile.read('/home/student/Desktop/SOUND.WAV')
        st = float(1/sr)
        chan = array.shape[1]
        le = array.shape[0] / sr
        ma = np.max(array[:, 0])
        print(st)
        print(chan)
        print(le)
        print(ma)
        array = array / (1<<8) + 128
        array = np.round(array)
        play(array[:, 0], st)
finally:
    light(0)
    gp.cleanup()
