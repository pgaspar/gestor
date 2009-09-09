var map;
var icon0;
var newpoints = new Array();

function addLoadEvent(func) { 
	var oldonload = window.onload; 
	if (typeof window.onload != 'function'){ 
		window.onload = func
	} else { 
		window.onload = function() {
			oldonload();
			func();
		}
	}
}

addLoadEvent(loadMap);
addLoadEvent(addPoints);

function loadMap() {
	map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
	map.addControl(new GMapTypeControl());
	map.setCenter(new GLatLng( 40.207861,-8.424411), 16);
	map.setMapType(G_SATELLITE_MAP);

	icon0 = new GIcon();
	icon0.image = "http://www.google.com/mapfiles/marker.png";
	icon0.shadow = "http://www.google.com/mapfiles/shadow50.png";
	icon0.iconSize = new GSize(20, 34);
	icon0.shadowSize = new GSize(37, 34);
	icon0.iconAnchor = new GPoint(9, 34);
	icon0.infoWindowAnchor = new GPoint(9, 2);
	icon0.infoShadowAnchor = new GPoint(18, 25);
}

function addPoints() {

	newpoints[0] = new Array(40.207861,-8.424411, icon0, 'Departamento de F&iacute;sica', 'Departamento de F&iacute;sica<br/>sala B3<br/>Rua Larga<br/>P-3004-516 Coimbra'); 

	for(var i = 0; i < newpoints.length; i++) {
		var point = new GPoint(newpoints[i][1],newpoints[i][0]);
		var popuphtml = newpoints[i][4] ;
		var marker = createMarker(point,newpoints[i][2],popuphtml);
		map.addOverlay(marker);
	}
}

function createMarker(point, icon, popuphtml) {
	var popuphtml = "<div id=\"popup\">" + popuphtml + "<\/div>";
	var marker = new GMarker(point, icon);
	GEvent.addListener(marker, "click", function() {
		marker.openInfoWindowHtml(popuphtml);
	});
	return marker;
}