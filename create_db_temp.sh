#!/usr/bin/env bash
set -eu

RRD_PATH="${RRD_PATH:-/home/pi/personal-weather-station/temperature.rrd}"
mkdir -p "$(dirname "$RRD_PATH")"

rrdtool create "$RRD_PATH" \
  --step 120 \
  DS:temp0:GAUGE:1200:-40:80 \
  RRA:AVERAGE:0.5:1:960 \
  RRA:MIN:0.5:96:3600 \
  RRA:MAX:0.5:96:3600 \
  RRA:AVERAGE:0.5:96:3600
