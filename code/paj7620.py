#author of this file is ehadley40
#the purpose of this script is to comunicate over i2c with the PAJ7620 sensor in the micropython language 

import time

#set chip settings
DEFAULT_ADDR = 0x73

REG_BANK_SEL = 0xEF
REG_CHIP_ID_L = 0x00
REG_CHIP_ID_H = 0x01
REG_GESTURE_FLAG = 0x43
REG_GESTURE_DATA = 0x44

GESTURES = { #this is the referance for the output
    0x01: "UP",
    0x02: "DOWN",
    0x04: "LEFT",
    0x08: "RIGHT",
    0x10: "FORWARD",
    0x20: "BACKWARD",
    0x40: "CLOCKWISE",
    0x80: "ANTICLOCKWISE",
    0x100: "WAVE"
}

INIT_REGISTERS = [ #initalizeing the registers
    (0xEF, 0x00),
    (0x32, 0x29), (0x33, 0x01), (0x34, 0x00), (0x35, 0x01),
    (0x36, 0x00), (0x37, 0x07), (0x38, 0x17), (0x39, 0x06),
    (0x3A, 0x12), (0x3F, 0x00), (0x40, 0x02), (0x41, 0xFF),
    (0x42, 0x01), (0x46, 0x2D), (0x47, 0x0F), (0x48, 0x3C),
    (0x49, 0x00), (0x4A, 0x1E), (0x4B, 0x00), (0x4C, 0x20),
    (0x4D, 0x00), (0x4E, 0x1A), (0x4F, 0x14), (0x50, 0x00),
    (0x51, 0x10), (0x52, 0x00),
    (0xEF, 0x01),
    (0x00, 0x1E), (0x01, 0x1E), (0x02, 0x0F),
    (0x03, 0x10), (0x04, 0x02), (0x05, 0x00),
    (0x06, 0xB0), (0x07, 0x04), (0x08, 0x0D),
    (0x09, 0x0E), (0x0A, 0x9C),
    (0x0B, 0x04), (0x0C, 0x05),
    (0x0D, 0x0F), (0x0E, 0x02),
    (0x0F, 0x12), (0x10, 0x02),
    (0x11, 0x02), (0x12, 0x00),
    (0x13, 0x01),
    (0xEF, 0x00)
]

class PAJ7620:
    def __init__(self, i2c, address=DEFAULT_ADDR, debug=False):
  #initalizes the sensor 
        self.i2c = i2c
        self.address = address
        self.debug = debug
        self._init_sensor()
        self.enable_gesture_mode()
    def _write(self, reg, val):
    #this is ther wirte fuuntion
        self.i2c.writeto(self.address, bytes([reg, val]))

    def _read(self, reg):
        #read funtion
        self.i2c.writeto(self.address, bytes([reg]))
        return self.i2c.readfrom(self.address, 1)[0]

    def _init_sensor(self):
   # Reset to bank 0
        self._write(REG_BANK_SEL, 0x00)
        time.sleep_ms(10)

        # Verify chip ID
        cid_l = self._read(0x00)
        cid_h = self._read(0x01)
        if self.debug:
            print("PAJ7620 Chip ID:", hex((cid_h << 8) | cid_l))

        # Full init table
        for reg, val in INIT_REGISTERS:
            self._write(reg, val)
            time.sleep_ms(1)

        # Enable gesture engine
        self.enable_gesture_mode()

        if self.debug:
            print("PAJ7620 init + gesture engine enabled")

    def enable_gesture_mode(self):
        # Switch to bank 1
        self._write(REG_BANK_SEL, 0x01)
        time.sleep_ms(5)

        # These registers enable gesture processing
        self._write(0x72, 0x01)
        self._write(0x73, 0x35)
        self._write(0x74, 0x00)
        self._write(0x75, 0x33)
        self._write(0x76, 0x31)
        self._write(0x77, 0x01)

        # Back to bank 0
        self._write(REG_BANK_SEL, 0x00)
        time.sleep_ms(5)

    def read_gesture(self):
        # Make sure we're in bank 0
        self._write(REG_BANK_SEL, 0x00)

        flag = self._read(0x43)
        data = self._read(0x44)

        if self.debug:
            print("RAW gesture regs -> flag:", hex(flag), "data:", hex(data))
        #outputs
        if flag == 0x01: return "UP"
        if flag == 0x02: return "DOWN"
        if flag == 0x04: return "LEFT"
        if flag == 0x08: return "RIGHT"
        if flag == 0x10: return "FORWARD"
        if flag == 0x20: return "BACKWARD"
        if flag == 0x40: return "CLOCKWISE"
        if flag == 0x80: return "ANTICLOCKWISE"

        return None
