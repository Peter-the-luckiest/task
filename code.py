import RPi.GPIO as GPIO
import time

ind = [24, 25, 8, 7, 12, 16, 20, 21]

def decToBinList(decNumber):
    x = []
    for _ in range(8):
        if decNumber % 2 == 1:
            x.append(1)
            decNumber = (decNumber-1)/2
        else:
            x.append(0)
            decNumber = decNumber/2
    return x


def lightUp(ledNumber, period):
    GPIO.output(ind[ledNumber], 1)
    time.sleep(period)
    GPIO.output(ind[ledNumber], 0)


def blink(ledNumber, blinkCount, blinkPeriod):
    for _ in range(blinkCount):
        GPIO.output(ind[ledNumber], 1)
        time.sleep(blinkPeriod)
        GPIO.output(ind[ledNumber], 0)
        time.sleep(blinkPeriod)


def runningLight(count, period):
    for _ in range(count):
        for j in range(8):
            GPIO.output(ind[(j-1)%8], 0)
            GPIO.output(ind[(j)%8], 1)
            time.sleep(period)
    GPIO.output(ind[7], 0)


def runningDark(count, period):
    for i in range(8):
        GPIO.output(ind[i], 1)
    for _ in range(count):
        for j in range(8):
            GPIO.output(ind[(j-1)%8], 1)
            GPIO.output(ind[(j)%8], 0)
            time.sleep(period)
    for i in range(8):
        GPIO.output(ind[i], 0)


def lightNumber(number):
    x = decToBinList(number)
    for i in range(8):
        if x[i] == 1:
            GPIO.output(ind[i], 1)
    time.sleep(3)
    for i in range(8):
        GPIO.output(ind[i], 0)


def runningPattern(pattern, direction):
    x = decToBinList(pattern)
    for _ in range(30):
        if direction == 0:
            a = x[0]
            for i in range(7):
                x[i] = x[(i+1)]
            x[7] = a
        else:
            a = x[7]
            for i in range(7, -1, -1):
                x[(i)%8] = x[(i-1)%8]
            x[0] = a
        for i in range(8):
            if x[i] == 1:
                GPIO.output(ind[i], 1)
        time.sleep(0.1)
        for i in range(8):
            GPIO.output(ind[i], 0)
    for i in range(8):
        GPIO.output(ind[i], 0)


def to_LED(number):
    p = GPIO.PWM(ind[number], 50)
    p.start(0)
    try:
        for _ in range(10):
            for dc in range(0, 101, 1):
                p.ChangeDutyCycle(dc)
                time.sleep(0.01)
            for dc in range(100, -1, -1):
                p.ChangeDutyCycle(dc)
                time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    p.stop()
    GPIO.cleanup()


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
n = int(input())
if n == 2:
    m = int(input())
    c = int(input())
    p = float(input())
    blink(m, c, p)
elif n == 3:
    c = int(input())
    p = float(input())
    runningLight(c, p)
elif n == 4:
    c = int(input())
    p = float(input())
    runningDark(c, p)
elif n == 5:
    m = int(input())
    print(decToBinList(m))
elif n == 6:
    m = int(input())
    lightNumber(m)
elif n == 7:
    m = int(input())
    d = int(input())
    runningPattern(m, d)
else:
    m = int(input())
    to_LED(m)
