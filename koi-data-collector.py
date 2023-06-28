#!/usr/bin/env python
import struct
import smbus
import sys
import os
import time
import glob
import board
import adafruit_sht31d
import RPi.GPIO as GPIO
from datetime import datetime

# Create I2C sensor object
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

file_path = "/home/pi/koipond/pond-data.txt"

temperature_sensor_1 = '/sys/bus/w1/devices/28-012114a4bd8f/w1_slave'
temperature_sensor_2 = '/sys/bus/w1/devices/28-0121146e2ac7/w1_slave'
temperature_sensor_3 = '/sys/bus/w1/devices/28-012114621451/w1_slave'

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def heat_sht31d_sensor():
    # Turn on the heater for 3 seconds
    sensor.heater = True
    time.sleep(1)
    sensor.heater = False

def read_temp(sensor_x):
    lines = read_temp_raw(sensor_x)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage

def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery"
        address = 0x36
        read = bus.read_word_data(address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity

def QuickStart(bus):
        address = 0x36
        bus.write_word_data(address, 0x06,0x4000)

def PowerOnReset(bus):
        address = 0x36
        bus.write_word_data(address, 0xfe,0x0054)

def output_battery(myList): # Write to the file
    f = open(file_path, "w")
    curr_dt = datetime.now()
    format = "%H:%M:%S %m-%d-%Y"
    #f.write(str(curr_dt(format)))
    f.write(curr_dt.strftime(format))
    f.write('\n')
    for element in myList:
         f.write(element)
         f.write('\n')
    f.close()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

PowerOnReset(bus)
QuickStart(bus)

time.sleep(2)
batteryVoltage = "Battery Voltage: %4.2f" % readVoltage(bus)
batteryPercentage = "Battery Percentage: %i" % readCapacity(bus)

if (readCapacity(bus) < 2):
	 os.system("sudo poweroff")

if (readCapacity(bus) > 100):
	batteryPercentage = "Battery Percentage: 100"

# Read temperature and humidity
ambient_temp_f = sensor.temperature * 9.0 / 5.0 + 32.0
#print("Ambient Temperature: %0.1f" % ambient_temp_f)
#print("Ambient Humidity: %0.1f" % sensor.relative_humidity)

s1 = "Temperature Pond-1: %4.2f" % read_temp(temperature_sensor_1)
s2 = "Temperature Pond-2: %4.2f" % read_temp(temperature_sensor_2)
s3 = "Temperature Pond-3: %4.2f" % read_temp(temperature_sensor_3)
s4 = "Ambient Temperature: %4.2f" % ambient_temp_f
s5 = "Ambient Humidity: %4.2f" % sensor.relative_humidity

myList = [batteryVoltage, batteryPercentage, s1, s2, s3, s4, s5]
time.sleep(10)
output_battery(myList)

heat_sht31d_sensor()
