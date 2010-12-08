#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use CGI::Pretty ":standard";
use CGI::Carp qw(carpout fatalsToBrowser);

my $JSURL;
if ($^O eq 'solaris') {
  $JSURL = 'http://www.stud.uni-giessen.de/~su9585/bilder.js';
}
else {
  $JSURL = '../bilder.js';
}

my $cgi = new CGI;
print $cgi->header();


print $cgi->start_html(-title => "Bilder von mir und anderen Leuten auch",
                       -script => {-type => 'text/javascript',
                                   -src  => $JSURL,},
                       -onLoad => "readColor();",
                      );

print <<HERE;
    <form method="post" action="login.cgi">
      <div style="position:fixed; top:0px; left:5px; width:100%; height:30px;" id="farbauswahl">
        <div style="position:relative; top:15px" align="center">
          <input type="button" name="style" value="weiss" class="knopf" onclick="weiss()">
          <input type="button" name="style" value="schwarz" class="knopf" onclick="schwarz()">
          <input type="button" name="style" value="zufall" class="knopf" onclick="zufall()">
        </div>
      </div>
    </form>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>
    <form method="post" action="passphrase.cgi">
      <p align="center">
        Passphrase:<br/>
        <input type="password" size="30" name="passphrase">
      </p>
    </form>
HERE

print $cgi->end_html();

