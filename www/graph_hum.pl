#!/usr/bin/perl
use strict;
use warnings;
use CGI qw(:standard);
use RRDs;

my $rrd = '/home/pi/personal-weather-station/humidity.rrd';
my $width = 1200;
my $height = 400;
my $query = CGI->new;
my $type = $query->param('type') || 'day';
$type = 'day' unless $type =~ /^(day|week|month|year)$/;

my $tmpfile = "/tmp/graph_humidity_$$.png";
my @opts = (
    '-v', '%',
    '-w', $width,
    '-h', $height,
    '-s', "now - 1 $type",
    '-e', 'now',
    '-D',
    '-t', 'Humidity',
    '-u', '100',
    '-l', '0',
    '-r',
);

RRDs::graph(
    $tmpfile,
    @opts,
    "DEF:hum0=$rrd:hum0:AVERAGE",
    'LINE2:hum0#0000FF:Humidity',
);

my $err = RRDs::error;
die "$err\n" if $err;

open(my $img, '<', $tmpfile) or die "can't open $tmpfile: $!\n";
print header(-type => 'image/png', -expires => '+1m');
local $/ = undef;
print <$img>;
close $img;
unlink $tmpfile;
