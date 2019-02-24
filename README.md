# Personal Weather Station
# Raspberry PI
## Set of scripts for temperature acquisition with DS18B20 temperature sensors.
## For enable Wire-1 in RaspPI:

add in /boot/config.txt:

dtoverlay=w1-gpio

add in # /etc/modules:

w1-gpio pullup=1

w1-therm

### Use lighttpd web server, rrdtool, perl and python for rrdtool:

sudo apt-get install librrds-perl lighttpd rrdtool python-rrdtool

## Enable :

sudo lighty-enable-mod cgi

sudo lighty-enable-mod userdir

### In /etc/lighttpd/conf-enabled/10-cgi.conf uncomment:

cgi.assign      = (
        ".pl"  => "/usr/bin/perl",
        ".py"  => "/usr/bin/python",
)

