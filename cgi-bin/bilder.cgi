#!/usr/bin/perl

# todo: * Bei Aufruf von login.cgi (ohne cookies?) wird in javascript farbe erwartet, aber undefined bekommen.
#       * Versuchen, Farbe schon beim Aufrufen der Seite anzuzeigen, und nicht erst, wenn alle Elemente geladen wurden.
#         Vielleicht geht das mit CSS. Über das Attribut style dürften sich die Werte ja danach noch ändern lassen.
#       * background-color -> background_color. Aber Achtung: In CSS heißt es ja wirklich background-color.
#
use strict;
use warnings;
use CGI qw(:standard :html3);
use CGI::Pretty qw(:standard);
use CGI::Carp qw(carpout fatalsToBrowser);
use File::Copy;

my $STARTSEITE = '../bilder';
my $BILDERORDNER = "../bilder";
my $BILDERORDNER700 = "../bilder/bilder700";
my $JSURL = '../bilder.js';
my $BILDERORDNERURL = $BILDERORDNER;

my $cgi = new CGI;

my $ordner = $cgi->param('ordner');

my $session_id = $cgi->cookie('session_id');
my $background_color = $cgi->cookie('background-color');
my $font_color = $cgi->cookie('font-color');
my $brighter_background_color;
my $darker_background_color;

$background_color =~ m/^.(..)(..)(..)$/;
my $r = $1;
my $g = $2;
my $b = $3;
my $brighter_r;
my $brighter_g;
my $brighter_b;
my $darker_r;
my $darker_g;
my $darker_b;

# Calculate the background color for the divs that underlie the buttons of every second month.
# This now are the bright colors.
if (hex($r) < 239) {
  $brighter_r = sprintf("%x", (hex($r)+16));
}
else {
  $brighter_r = 'ff';
}
if (hex($g) < 239) {
  $brighter_g = sprintf("%x", (hex($g)+16));
}
else {
  $brighter_g = 'ff';
}
if (hex($b) < 239) {
  $brighter_b = sprintf("%x", (hex($b)+16));
}
else {
  $brighter_b = 'ff';
}
$brighter_background_color = "#$brighter_r$brighter_g$brighter_b";

# These are the dark ones.
if (hex($r) > 16) {
  $darker_r = sprintf("%x", (hex($r)-16));
}
else {
  $darker_r = '00';
}
if (hex($g) > 16) {
  $darker_g = sprintf("%x", (hex($g)-16));
}
else {
  $darker_g = '00';
}
if (hex($b) > 16) {
  $darker_b = sprintf("%x", (hex($b)-16));
}
else {
  $darker_b = '00';
}
$darker_background_color = "#$darker_r$darker_g$darker_b"; 

my $css_code = "body {background-color:$background_color; color:$font_color}";

my $time_times_666 = &time_times_666();

my $title_ordner_bezeichnung = defined $ordner ? ": $ordner" : '';

  print $cgi->header(-charset=>'UTF-8');
  print $cgi->start_html(-title => "Bilder von mir und anderen Leuten auch".$title_ordner_bezeichnung,
                         -script => {-type => 'text/javascript',
                                     -src  => $JSURL,},
                         -style => {-code => $css_code,},
                         -onLoad => "readColor();",
                        );

if ($session_id ne $time_times_666) {
	print $cgi->h2("Aktivieren Sie Cookies in Ihrem Browser und loggen sie sich auf der <a href='$STARTSEITE'>Startseite</a> ein.");
}
if ($session_id eq $time_times_666) {
	opendir(BILDERORDNER, $BILDERORDNER);
	my @bilderordnerordner = readdir(BILDERORDNER);
	closedir(BILDERORDNER);

	my @bilddateien;

	foreach(@bilderordnerordner) {
		if (not $_ =~ m/html|700/ and not $_ =~ m/^\.\.?$/) {
			system("chmod -R a+rx $BILDERORDNER/$_");
			push(@bilddateien, $_);
		}
	}
  	@bilderordnerordner = @bilddateien;

print <<HERE;
        <div style="position:relative; top:5px; z-index:8;" align="center" id="farbauswahl">
          <input type="button" name="style" value="weiss" class="knopf" onclick="weiss()">
          <input type="button" name="style" value="schwarz" class="knopf" onclick="schwarz()">
          <input type="button" name="style" value="zufall" class="knopf" onclick="zufall()">
        </div>
HERE


  print '<div style="position:absolute; top:50px; left:5px; width:115px; height:100%; background-color:'.$background_color.'" id="ordnerauswahl">
  <div align="center">'."\n";
	print $cgi->start_form(-method => 'POST',
        				       -action => 'bilder.cgi',
        				       -name => 'ordner',
              		       );
  my $vorheriger_monat = 0; # Defaultvalue at the beginning.
  my @background_colors = ($brighter_background_color, $darker_background_color);
  my @background_brightnesses = qw(bright dark);
  my $counter = 0;
  foreach my $bilderordner (reverse(sort(@bilderordnerordner))) {
    $bilderordner =~ m/^\d+\.(\d\d?)\..+$/;
    my $aktueller_monat = $1;
    $aktueller_monat =~ s/^0//;
  	if ($aktueller_monat != $vorheriger_monat) {
  	  my $index = $aktueller_monat % 2;
  	  print "</div>\n" if $vorheriger_monat != 0;
  	  print "<div style='background-color:$background_colors[$index]' id='$background_brightnesses[$index]_background_$counter'>"."\n";
  	  $counter++;
  	  $vorheriger_monat = $aktueller_monat;
    }
	if (defined $ordner and $ordner eq $bilderordner) {
	 	print $cgi->submit(-name => 'ordner',
		                   -value => $bilderordner,
							 -style=>'background-color:#cbcbcb',
 		       			    );
	}
	else {
	 	print $cgi->submit(-name => 'ordner',
		                   -value => $bilderordner,
	 	       			    );
	}
 	  print "\n";
  }
  print "</div>"."\n";
		print $cgi->end_form();
    print "</div></div>"."\n";


  # In case we clicked onto a button with a date
  if (defined $ordner) {
    opendir(BILDER, "$BILDERORDNER/$ordner");
    my @bilder = readdir(BILDER);
    closedir(BILDER);
    print '<div style="position:relative; top:50px; left:140px; width:800px; height:100%; z-index:1;" id="bild">'."\n";
    foreach my $bild (@bilder) {
      if (not $bild =~ /^\.\.?$/) { # If file is not '.' and not '..'.
        if ($bild =~ m/\.\w+$/) {
          if (not -d "$BILDERORDNER700/$ordner") {
            mkdir("$BILDERORDNER700/$ordner") or die $!;
            chmod(0777, "$BILDERORDNER700/$ordner") or die $!;
          }
          if (not -f "$BILDERORDNER700/$ordner/$bild") {
            my $unixpath = "$BILDERORDNER/$ordner/$bild";
               $unixpath =~ s/ /\\ /g;
            my $unixpath700 = "$BILDERORDNER700/$ordner/$bild";
               $unixpath700 =~ s/ /\\ /g;
            $bild =~ m/.+\.(\w+)$/;
            my $pnm2extension = 'pnmto'.lc($1);
            my $extension2pnm = lc($1).'topnm';
            $pnm2extension =~ s/jpg/jpeg/;
            $extension2pnm =~ s/jpg/jpeg/;
            # We want the info about the file.
            my $fileinfo = qx($extension2pnm 2>> pnm.log $unixpath | pnmfile);
            $fileinfo =~ m/(\d+) by (\d+)/;
            my $original_filewidth = $1;
            my $original_fileheight = $2;
            my $new_filewidth = 700;
            # Because we don't know if the picture is in landscape or portrait format, we have to calculate
            # the new height. It is shrinked (or maybe raised) by the same factor as the new width relative to the
            # old one.
            my $new_fileheight = int($original_fileheight / ($original_filewidth/$new_filewidth));
            system("$extension2pnm 2>> pnm.log $unixpath | pnmscale -xysize $new_filewidth $new_fileheight | $pnm2extension > $unixpath700");
          }
        }
        
        ################################
        # In case of nested directories.
        if (not $bild =~ /\.\w+$/) {
          print $cgi->start_form(-method => 'POST',
                     -action => 'bilder.cgi',
                     -name => 'ordner',
                     -value => "$ordner/$bild",
                     );
          print $cgi->submit(
                     -name => 'ordner',-value => "$ordner/$bild",
                );
          print $cgi->end_form();
          print $cgi->br();
        }
        # The normal case. Print out the shrinked picture with a link to the original file.
        else {
          print "<a href='$BILDERORDNERURL/$ordner/$bild'><img width='700' src='$BILDERORDNERURL/bilder700/$ordner/$bild'></a><br/><br/>\n";
#          print "<a href='$BILDERORDNERURL/$ordner/$bild'><img width='700' src='http://www.stud.uni-giessen.de/~su9585/chimage.php?image=$bild'></a><br/><br/>\n";
        }
        ###################################
      }
    }
    print "</div>\n";
  }
}

print $cgi->end_html();

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
