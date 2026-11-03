#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use RRDs;

my $rrd = '/home/pi/personal-weather-station/temperature.rrd';
my $width = 1200;
my $height = 400;
my $query = CGI->new;
my $type = $query->param('type') || 'day';
$type = 'day' unless $type =~ /^(day|week|month|year)$/;

my $tmpfile = "/tmp/graph_temperature_$$.png";
my @opts = (
    '-v', '°C',
    '-w', $width,
    '-h', $height,
    '-s', "now - 1 $type",
    '-e', 'now',
    '-D',
    '-t', 'Temperature',
    '-u', '80',
    '-l', '-20',
    '-r',
);

RRDs::graph(
    $tmpfile,
    @opts,
    "DEF:temp0=$rrd:temp0:AVERAGE",
    'LINE2:temp0#00CC66:Temperature',
);

my $err = RRDs::error;
die "$err\n" if $err;

open(my $img, '<', $tmpfile) or die "can't open $tmpfile: $!\n";
print header(-type => 'image/png', -expires => '+1m');
local $/ = undef;
print <$img>;
close $img;
unlink $tmpfile;
