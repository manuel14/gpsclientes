$(document).ready(function() {
    $(window).on('load', function() {
        initMap();
        dibujar();
    });
}); 
    var initMap = function initMap() {
        map = new google.maps.Map($('#map')[0], {
            center: {lat: -54.807134, lng: -68.300865},
            zoom: 12
        });
    }
    var dibujar =  function() {
        var locations = new Array();
        //Básico
        $.each(data, function(index, val){
            var dic = {};
            var dic_position = {"lat": val.lat, "lng": val.long}
            dic.position=dic_position;
            dic.clientenro=val.clientenro.toString();
            locations.push(dic);
        });
        var markers = locations.map(function(location, i) {
          return new google.maps.Marker({
            position: location.position,
            label: location.clientenro,
          });
        });
        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
        }
