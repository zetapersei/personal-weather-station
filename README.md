# personal-weather-station

## in Raspberry PI

### Use lighttpd web server, rrdtool, perl and python for rrdtool.

- (sudo apt-get install librrds-perl lighttpd rrdtool python-rrdtool):

## Enable :

sudo lighty-enable-mod cgi

sudo lighty-enable-mod userdir

## In /etc/lighttpd/conf-enabled/10-cgi.conf uncomment:

cgi.assign      = (
        ".pl"  => "/usr/bin/perl",
        ".py"  => "/usr/bin/python",
)

