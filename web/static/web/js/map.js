$(document).ready(function() {
	$(window).on('load', function() {
		dibujar();
	});
});

colors = shuffle(['#F44336','#FF4081','#2196F3','#009688','#FFC107','#795548','#607D8B','#4CAF50','#3F51B5','#E040FB','#FF5722'])

var dibujar = function() {
	var markers = [];
	var lines = [];
	var color = getColor();
	var lat_lng = new Array();
	var latlngbounds = new google.maps.LatLngBounds();
	if (!data.length) {
		alert('No hay clientes aún');
		window.close();
		return;
	}
	$.each(data, function(index, val) {
		var time = moment(val[3]);
		var myLatLng = new google.maps.LatLng(val[0], val[1]);
		lat_lng.push(myLatLng);
		var content = '<div id="content">'+
			'<h6>Nro cliente: '+val[5]+'</h6>'+
			'<h6>Nombre: '+val[2]+'</h6>'+
			'<h6>Direccion: '+val[4]+'</h6>'+
			'</div>';
		var infowindow = new google.maps.InfoWindow({
			content: content
		});
		var marker = new google.maps.Marker({
			position: myLatLng,
			map: map,
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 5,
				strokeWeight: 2,
				fillColor:color,
				strokeColor:'#FFFFFF',
				fillOpacity:1
			}
		});
		marker.addListener('mouseover',function() {
			infowindow.open(map,marker);
		});
		marker.addListener('mouseout',function() {
			infowindow.close(map,marker);
		});
		markers.push(marker);
		latlngbounds.extend(marker.position);
	});
	map.setCenter(latlngbounds.getCenter());
	map.fitBounds(latlngbounds);
	var line = new google.maps.Polyline({
		path: lat_lng,
		geodesic: true,
		strokeColor: color,
		strokeOpacity: 1.0,
		strokeWeight: 2
	})
	lines.push(line);
	line.setMap(map);
}

var limpiar = function(markers,lines) {
	$.each(markers, function(index, val) {
		val.setMap(null);
	});
	markers.length = 0;
	$.each(lines, function(index, val) {
		val.setMap(null);
	});
	lines.length = 0;
}

function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
    return a;
}

var getColor = function() {
	return colors.pop();
}