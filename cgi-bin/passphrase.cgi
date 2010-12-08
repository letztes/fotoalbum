#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Pretty ":standard";
use CGI::Carp qw(carpout fatalsToBrowser);

my $cgi = new CGI;

my $passphrase_count_file_name = "passphrase_count.txt";
my $passphrase_count_file_handle;

if (-f $passphrase_count_file_name) {
    # first read the time to sleep
    open($passphrase_count_file_handle, "passphrase_count.txt");
    my $passphrase_count = <$passphrase_count_file_handle>;
    close($passphrase_count_file_handle);
    
    # then write double the value back to file
    open($passphrase_count_file_handle, ">passphrase_count.txt");
    print $passphrase_count_file_handle $passphrase_count*2+1;
    close($passphrase_count_file_handle);
    sleep $passphrase_count;
}
else {
    open($passphrase_count_file_handle, ">passphrase_count.txt");
    print $passphrase_count_file_handle 0;
    close($passphrase_count_file_handle);
}

my $background_color = $cgi->cookie('background-color');
my $font_color = $cgi->cookie('font-color');

my $passphrase = $cgi->param('passphrase');

my $time_times_666 = &time_times_666();

# replace XXX with your passphrase
#if ($passphrase =~ /^XXX$/i) {
if ($passphrase eq 'XXX') {
    # set "time to sleep" to 0
    open($passphrase_count_file_handle, ">passphrase_count.txt");
    print $passphrase_count_file_handle 0;
    close($passphrase_count_file_handle);
    
	my $cookie = $cgi->cookie(-name => 'session_id',
				  -value => $time_times_666,
          -expires => '+1d',
				 );
	print $cgi->header(-charset => 'UTF-8',
			   -cookie => $cookie,);
	print '<html><head><meta http-equiv="Refresh" content="0; URL=bilder.cgi">
</head><body></body></html>';

	
}
else {
    
    
	print $cgi->header(-charset => 'UTF-8',);
	print $cgi->start_html(-head => style({type => 'text/css'},
	                                      "body{background-color : $background_color; color : $font_color;}",
	                                      ),
	                      );
	print "<p align='center'>";
	print "<h3>falsches Passwort</h3>";
	print "</p>";
	print $cgi->end_html();
}

sub time_times_666 {
	my $time = localtime(time);
	my @tokens = split(/ /, $time);
	my $day;
	for(0..2) {
		$day .= $tokens[$_];
	}
	my @characters = split('', $day);

	my $time_times_666 = 0;

	foreach(@characters) {
		$time_times_666 += ord($day) * 666;
	}
	return $time_times_666;
}
