function initMap() {
	map = new google.maps.Map($('#map')[0], {
		center: {lat: -54.807134, lng: -68.300865},
		zoom: 12
	});
}