#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os, rrdtool, time, Adafruit_DHT, MySQLdb

humidity, temperature = Adafruit_DHT.read_retry(11, 14) 
print (humidity) 

# read sensor data data = 'N'

data += ':'
data += str(humidity)
time.sleep(1)

# insert data into round-robin-database
rrdtool.update(
  "/home/pi/personal-weather-station/humidity.rrd",
data)
# Connection Database Mysql
db = MySQLdb.connect("localhost","user","passwd","weather") 
# Optained cursor 
cursor = db.cursor() 

sql = "INSERT INTO wr_humidity (sensor_id, value) " "VALUES(6, %u)" % humidity

try:
   # SQL query execution
   cursor.execute(sql)
   # Commit
   db.commit()
except:
# Rollback if error
   db.rollback()

# Database disconnection
db.close()
