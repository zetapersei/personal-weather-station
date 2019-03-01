#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os, rrdtool, time, Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(11, 14)

# read sensor data
data = 'N'

data += ':'
data += humidity
time.sleep(1)

# insert data into round-robin-database
rrdtool.update(
  "/home/pi/personal-weather-station/humidity.rrd",
data)
