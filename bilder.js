
var background_color;
var font_color;

function weiss()
{
  background_color='#ffffff';
  font_color='#000000';
  var dark_background_color = '#eeeeee';
  var bright_background_color = background_color;
  set_color(background_color, dark_background_color, bright_background_color, font_color);
}

function schwarz()
{
  background_color='#000000';
  font_color='#ffffff';
  var dark_background_color = background_color;
  var bright_background_color = '#3f3f3f';
  set_color(background_color, dark_background_color, bright_background_color, font_color);
}

function zufall()
{
  var hex_array = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f');
  red = parseInt( Math.random() * ( 256 ) );
  grn = parseInt( Math.random() * ( 256 ) );
  blu = parseInt( Math.random() * ( 256 ) );
  
  hex_red = Number(red).toString(16);
  hex_grn = Number(grn).toString(16);
  hex_blu = Number(blu).toString(16);
  
  dark_red = red-16;
  dark_grn = grn-16;
  dark_blu = blu-16;
  
  dark_hex_red = Number(dark_red).toString(16);
  dark_hex_grn = Number(dark_grn).toString(16);
  dark_hex_blu = Number(dark_blu).toString(16);
  
  if (dark_hex_red.length == 1) {dark_hex_red = '0'+dark_hex_red}
  if (dark_hex_grn.length == 1) {dark_hex_grn = '0'+dark_hex_grn}
  if (dark_hex_blu.length == 1) {dark_hex_blu = '0'+dark_hex_blu}
  
  bright_red = red+16;
  bright_grn = grn+16;
  bright_blu = blu+16;
  
  bright_hex_red = Number(bright_red).toString(16);
  bright_hex_grn = Number(bright_grn).toString(16);
  bright_hex_blu = Number(bright_blu).toString(16);
  
  if (red < 17) {
    hex_red = '0'+hex_red;
    dark_hex_red = '00';
  }
  if (grn < 17) {
    hex_grn = '0'+hex_grn;
    dark_hex_grn = '00';
  }
  if (blu < 17) {
    hex_blu = '0'+hex_blu;
    dark_hex_blu = '00';
  }
  
  if (red > 239) {
    bright_hex_red = 'ff';
  }
  if (grn > 239) {
    bright_hex_grn = 'ff';
  }
  if (blu > 239) {
    bright_hex_blu = 'ff';
  }
  
  background_color='#'+hex_red+hex_grn+hex_blu;
  dark_background_color = '#'+dark_hex_red+dark_hex_grn+dark_hex_blu;
  bright_background_color = '#'+bright_hex_red+bright_hex_grn+bright_hex_blu;
  
  if ((red > 127 && grn > 127) || (red > 127 && blu > 127) || (grn > 127 && blu > 127)) {
    font_color='#000000';
  }
  else {
    font_color='#ffffff';
  }
  set_color(background_color, dark_background_color, bright_background_color, font_color);
}

function readColor() {
  cookies = document.cookie;

  cookies.replace(/\s/g,'');
  
  // Read and set the background_color.
  cookiename1 = cookies.substring(0,cookies.search('='));
  if (cookies.search(';') != -1) {cookiewert1 = cookies.substring(cookies.search('=')+1,cookies.search(';'));}
  else {cookiewert1 = cookies.substring(cookies.search('=')+1,cookies.length);}
  if(cookiewert1 == '') {cookiewert1 = cookies.substring(cookies.search('=')+1,cookies.length);}
  
  if (cookiename1.match(/background-color/)) {
    background_color = cookiewert1;
  }
  else {
    weiss();
    return;
  }
  
  // Read and set the dark_background_color.
  cookies = cookies.substring(cookies.search(';')+1,cookies.length);

  cookiename2 = cookies.substring(0,cookies.search('='));
  if (cookies.search(';') != -1) {cookiewert2 = cookies.substring(cookies.search('=')+1,cookies.search(';'));}
  else {cookiewert2 = cookies.substring(cookies.search('=')+1,cookies.length);}
  if(cookiewert2 == '') {cookiewert2 = cookies.substring(cookies.search('=')+1,cookies.length);}

  if (cookiename2.match(/dark_background_color/)) {
    dark_background_color = cookiewert2;
  }
  else {
    weiss();
    return;
  }
  
  // Read and set the bright_background_color.
  cookies = cookies.substring(cookies.search(';')+1,cookies.length);

  cookiename3 = cookies.substring(0,cookies.search('='));
  if (cookies.search(';') != -1) {cookiewert3 = cookies.substring(cookies.search('=')+1,cookies.search(';'));}
  else {cookiewert3 = cookies.substring(cookies.search('=')+1,cookies.length);}
  if(cookiewert3 == '') {cookiewert3 = cookies.substring(cookies.search('=')+1,cookies.length);}

  if (cookiename3.match(/bright_background_color/)) {
    bright_background_color = cookiewert3;
  }
  else {
    weiss();
    return;
  }
  
  // Read and set the font_color.
  cookies = cookies.substring(cookies.search(';')+1,cookies.length);

  cookiename4 = cookies.substring(0,cookies.search('='));
  if (cookies.search(';') != -1) {cookiewert4 = cookies.substring(cookies.search('=')+1,cookies.search(';'));}
  else {cookiewert4 = cookies.substring(cookies.search('=')+1,cookies.length);}
  if(cookiewert4 == '') {cookiewert4 = cookies.substring(cookies.search('=')+1,cookies.length);}
  
  if (cookiename4.match(/font-color/)) {
    font_color = cookiewert4;
  }
  else {
    weiss();
    return;
  }
  
  set_color(background_color, dark_background_color, bright_background_color, font_color);
}

function set_color(background_color, dark_background_color, bright_background_color, font_color) {
  document.body.style.color=font_color;
  document.body.style.backgroundColor=background_color;
  document.getElementById('farbauswahl').style.backgroundColor=background_color;
  document.getElementById('farbauswahl').style.color=font_color;
  
  // set background color to all the divs with bright background
  var counter = 1;
  while (document.getElementById('bright_background_'+counter)) {
    document.getElementById('bright_background_'+counter).style.backgroundColor=bright_background_color;
    counter += 2;
  }
  // set background color to all the divs with dark background
  counter = 0;
  while (document.getElementById('dark_background_'+counter)) {
    document.getElementById('dark_background_'+counter).style.backgroundColor=dark_background_color;
    counter += 2;
  }
  
  if (document.getElementById('ordnerauswahl')) {
    document.getElementById('ordnerauswahl').style.backgroundColor=background_color;
    document.getElementById('ordnerauswahl').style.color=font_color;
  }
  
  // set color values to cookies
  var a = new Date();
  a = new Date(a.getTime() +1000*60*60*24*365);
  document.cookie = 'background-color='+background_color+'; expires='+a.toGMTString()+';'; 
  document.cookie = 'dark_background_color='+dark_background_color+'; expires='+a.toGMTString()+';'; 
  document.cookie = 'bright_background_color='+bright_background_color+'; expires='+a.toGMTString()+';'; 
  document.cookie = 'font-color='+font_color+'; expires='+a.toGMTString()+';';
}
