this library is a micro python library that handles I2C control over the PAJ7620 hand gesture sensor. it is my first and a very basic library but it has done well for my projects and i hope it does well for yours as well

## Installation
Esp 32 or RPI Pico
1. copy the code from the file named PAJ7620
2. open thony on a blank page and paste in the code
3.  hit save or ctrl + s
4. there will be 2 options they vary depending on your devices but you want to click the one that is not your computer. it may be under micro python device or the name of your micro controller 
5. name the file paj7620.py and hit OK
6. DONE
## USE
this lib has one function
```python
paj7620.PAJ7620(i2c, address=DEFAULT_ADDR, debug=False)
```
this function has a few main parts first and most important is the i2c  you need to the command what i2c bus to refer to i find it easier to configure it and name it i2c i then place that variable name in place like so
```python
i2c_guesture = machine.I2C(1, scl=machine.Pin(22), sda=machine.pinPin(21), freq=100000)

paj7620.PAJ7620(i2c_guesture,)

```

the address statement is only necessary if you run other devices on the i2c bus and there addresses clash meaning that the address is different to what is normal. the usual address for this sensor is 0x73. 

the debug statement is only necessary if you are having problems with the sensor or with configuring the bus. this debug mode is off by default and outputs an init log and flag and data values into the serial terminal. 

### outputs

this function out puts a few different outputs and the out put is read off the flag value not data(for debugging purposes)

in the following graph you dont need to know the hex values only the output values unless you plan on editing my library

| output        | hexvalue |
| ------------- | -------- |
| UP            | 0x01     |
| DOWN          | 0x02     |
| LEFT          | 0x04     |
| RIGHT         | 0x08     |
| FORWARD       | 0x10     |
| BACKWARD      | 0x20     |
| ANITCLOCKWISE | 0x80     |
| CLOCKWISE     | 0x40     |
| WAVE          | 0x100    |

