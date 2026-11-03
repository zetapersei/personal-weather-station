#!/usr/bin/env python3

import re
import sys
import time
from pathlib import Path

import rrdtool

try:
    import MySQLdb
except ModuleNotFoundError:  # pragma: no cover - optional dependency at runtime
    MySQLdb = None

SENSOR_PATH = Path("/sys/bus/w1/devices/28-0417c3a4e1ff/w1_slave")
RRD_PATH = Path("/home/pi/personal-weather-station/temperature.rrd")
DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "passwd": "passwd",
    "db": "weather",
}


def read_sensor(path):
    """Read the DS18B20 temperature value from a 1-Wire slave file."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as exc:
        print(f"{time.strftime('%x %X')} Error reading {path}: {exc}", file=sys.stderr)
        return None

    if len(lines) < 2:
        return None

    first_line = lines[0].strip()
    second_line = lines[1].strip()
    if not re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", first_line):
        return None

    match = re.search(r"t=([+-]?[0-9]+)", second_line)
    if match is None:
        return None

    return float(match.group(1)) / 1000.0


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
            "INSERT INTO wr_temperature (sensor_id, value) VALUES (%s, %s)",
            (6, round(float(value), 3)),
        )
        db.commit()
        db.close()
        return True
    except MySQLdb.Error as exc:
        print(f"Database insertion failed: {exc}", file=sys.stderr)
        return False


def main():
    value = read_sensor(SENSOR_PATH)
    if value is None:
        print("Unable to read temperature sensor.", file=sys.stderr)
        return 1

    update_rrd(value)
    insert_database(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
