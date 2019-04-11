#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, os, rrdtool, time, Adafruit_DHT, MySQLdb

humidity, temperature = Adafruit_DHT.read_retry(11, 14) print (humidity) # read sensor data data = 'N'

data += ':'
data += str(humidity)
time.sleep(1)

# insert data into round-robin-database
rrdtool.update(
  "/home/pi/personal-weather-station/humidity.rrd",
data)
# Coonection Database Mysq
db = MySQLdb.connect("localhost","user","passwd","weather" ) # Ottenimento del cursore cursor = db.cursor() sql = "INSERT INTO wr_humidity (sensor_id, value) " "VALUES(6, %u)" % humidity

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
