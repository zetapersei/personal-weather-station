#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os, rrdtool, time, Adafruit_DHT, MySQLdb

sensor = Adafruit_DHT.DHT11
pin = 14

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# function: read and parse sensor data file def read_sensor(path):
  value = "U"
  try:
    f = open(path, "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(float(m.group(2)) / 1000.0)
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value

# define pathes to 1-wire sensor data
path = (
  "/sys/bus/w1/devices/28-0417c3a4e1ff/w1_slave"
)

# print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

# read sensor data
data = 'N'
data += ':'
data += read_sensor(path)
time.sleep(1)

# insert data into round-robin-database
rrdtool.update(
  "/home/pi/personal-weather-station/temperature.rrd",
  data)
# Connessione al Database
db = MySQLdb.connect("localhost","user","passwd","weather" ) # Ottenimento del cursore cursor = db.cursor() sql = "INSERT INTO wr_temperature (sensor_id, value) VALUES(6, %.1f)" % float(read_sensor(path))

try:
   # Esecuzione della query SQL
   cursor.execute(sql)
   # Commit
   db.commit()
except:
   # Rollback in caso di errore
   db.rollback()

# Disconnessione
db.close()
