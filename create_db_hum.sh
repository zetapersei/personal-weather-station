#!/usr/bin/env bash
set -eu

RRD_PATH="${RRD_PATH:-/home/pi/personal-weather-station/humidity.rrd}"
mkdir -p "$(dirname "$RRD_PATH")"

rrdtool create "$RRD_PATH" \
  --step 120 \
  DS:hum0:GAUGE:1200:0:100 \
  RRA:AVERAGE:0.5:1:960 \
  RRA:MIN:0.5:96:3600 \
  RRA:MAX:0.5:96:3600 \
  RRA:AVERAGE:0.5:96:3600
