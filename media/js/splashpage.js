var duration = 200;  /* 1000 millisecond fade = 1 sec */
var steps = 20;       /* number of opacity intervals   */

function fadeIn(id){
  for (i = 0; i <= 1; i += (1 / steps)) {
    setTimeout("setOpacity( $('" + id + "'), " + i + ")", i * duration);
  }
}

/* set the opacity of the element (between 0.0 and 1.0) */
function setOpacity(element, level) {
  element.style.opacity = level;
  element.style.MozOpacity = level;
  element.style.KhtmlOpacity = level;
  element.style.filter = "alpha(opacity=" + (level * 100) + ");";
}

function show_auth() {
	$('auth-link').hide();
	$('auth-form').show();
	fadeIn( 'auth-form' );
	$('id_username').focus();
}

var faded = false;
var movecount = 0;

function fade() {
	movecount++;
	
	if (!faded && movecount > 1) {
		fadeIn('social');
		fadeIn('auth');
		faded = true;
	}
}