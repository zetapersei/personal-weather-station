#!/usr/bin/perl
#
# CGI script to create image using RRD graph 
use CGI qw(:all);
use RRDs;
use strict;

# path to database
my $rrd='/home/pi/personal-weather-station/temperature.rrd';
my $rrd_hum='/home/pi/personal-weather-station/humidity.rrd';

# size
my $width=1200;
my $height=400;

# read and check query params
my $query=new CGI;
my $type=$query->param('type');
$type='day' unless $type =~ /day|week|month|year/;

# write image into temp file
my $tmpfile="/tmp/graphx_$$.png";
my @opts=("-v", "°C",
"-w", $width,
"-h", $height,
"-s", "now - 1 $type",
"-e", "now",
"-D");
RRDs::graph($tmpfile,
  @opts,
  "DEF:temp0=$rrd:temp0:AVERAGE",
  "LINE2:temp0#00FF00:Inside"
   "DEF:hum0=$rrd_hum:hum0:AVERAGE",
  "LINE2:hum0#0000FF:Humidity"
);
# check error
my $err=RRDs::error;
die "$err\n" if $err;

# feed tmpfile to stdout
open(IMG, $tmpfile) or die "can't open $tmpfile\n";
print header(-type=>'image/png', -expires=>'+1m');
print <IMG>;
close IMG;
unlink $tmpfile;
