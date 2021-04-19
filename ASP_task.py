import RPi.GPIO as gp
import time 
import numpy as np

pins = [10, 9, 11, 5, 6, 13, 19, 26]
pinz = [24, 25, 8, 7, 12, 16, 20, 21]
gp.setmode(gp.BCM)
gp.setup(pins, gp.OUT)
gp.setup(4, gp.IN)
gp.setup(17, gp.OUT)
gp.setup(pinz, gp.OUT)


def to_bin(val):
    out = [0] * 8
    for i in range(7, -1, -1):
        if val // 2 ** i != 0:
            out[i] = 1
            val %= 2 ** i
    return out


def num_dac(val):
    array = to_bin(val)
    gp.output(17, 1)
    gp.output(pins, array)


def first():
    while True:    
        num = int(input("Enter value (-1 to exit) > "))
        if num == -1:
            break
        num_dac(0)
        num_dac(num)
        print(num, " = ", round(3.3/255*num, 2), "V", sep="")


def second():
    while True:
        for i in range(256):
            num_dac(0)
            num_dac(i)
            time.sleep(0.01)
            if gp.input(4) == 0:
                print("Digital value: ", i, "Analog value: ", round(3.3/255*i, 2), "V")
                break


def third():
    while True:
        r = 255
        l = 0
        while r-l > 1:
            num_dac(0)
            num_dac(r)
            time.sleep(0.01)
            w = gp.input(4)
            num_dac(0)
            num_dac(l)
            time.sleep(0.01)
            q = gp.input(4)
            cur = (r+l)//2
            num_dac(0)
            num_dac(cur)
            time.sleep(0.01)
            e = gp.input(4)
            if e != w:
                l = cur
            else:
                r = cur
        print("Digital value: ", r, "Analog value: ", round(3.3/255*r, 2), "V")


def fourth():
    while True:
        r = 255
        l = 0
        while r-l > 1:
            num_dac(0)
            num_dac(r)
            time.sleep(0.01)
            w = gp.input(4)
            num_dac(0)
            num_dac(l)
            time.sleep(0.01)
            q = gp.input(4)
            cur = (r+l)//2
            num_dac(0)
            num_dac(cur)
            time.sleep(0.01)
            e = gp.input(4)
            if e != w:
                l = cur
            else:
                r = cur
        print("Digital value: ", r, "Analog value: ", round(3.3/255*r, 2), "V")
        ma = 253
        mi = 1
        st = (ma-mi)/8
        out = [0] * 8
        gp.output(pinz, out)
        for i in range(round((r-1)/st)):
            out[i] = 1
        gp.output(pinz, out)


try:
    if __name__ == "__main__":
        fourth()
finally:
    num_dac(0)
    gp.cleanup()
