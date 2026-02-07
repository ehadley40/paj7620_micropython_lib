from machine import I2C, Pin
from paj7620 import PAJ7620
import time

i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)

sensor = PAJ7620(i2c)

while True:
    g = sensor.read_gesture()
    if g:
        print("Gesture:", g)
    time.sleep(0.1)
