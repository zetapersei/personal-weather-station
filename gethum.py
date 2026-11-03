#!/usr/bin/env python3

import sys
import time
from pathlib import Path

import rrdtool

try:
    import Adafruit_DHT
except ModuleNotFoundError:  # pragma: no cover - optional dependency at runtime
    Adafruit_DHT = None

try:
    import MySQLdb
except ModuleNotFoundError:  # pragma: no cover - optional dependency at runtime
    MySQLdb = None

SENSOR_PIN = 14
SENSOR_TYPE = 11
RRD_PATH = Path("/home/pi/personal-weather-station/humidity.rrd")
DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "passwd": "passwd",
    "db": "weather",
}


def read_humidity():
    if Adafruit_DHT is None:
        print("Adafruit_DHT is not installed. Cannot read humidity sensor.", file=sys.stderr)
        return None

    humidity, _temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
    if humidity is None:
        print(f"{time.strftime('%x %X')} Failed to read humidity sensor.", file=sys.stderr)
        return None
    return float(humidity)


def update_rrd(value):
    try:
        rrdtool.update(str(RRD_PATH), f"N:{value:.3f}")
    except rrdtool.OperationalError as exc:
        print(f"RRD update failed: {exc}", file=sys.stderr)
        return False
    return True


def insert_database(value):
    if MySQLdb is None:
        print("MySQLdb is not installed. Skipping database insertion.", file=sys.stderr)
        return False

    try:
        db = MySQLdb.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO wr_humidity (sensor_id, value) VALUES (%s, %s)",
            (6, round(float(value), 3)),
        )
        db.commit()
        db.close()
        return True
    except MySQLdb.Error as exc:
        print(f"Database insertion failed: {exc}", file=sys.stderr)
        return False


def main():
    value = read_humidity()
    if value is None:
        return 1

    update_rrd(value)
    insert_database(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
