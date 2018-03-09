$(document).ready(function() {
    $(window).on('load', function() {
        dibujar();
    });
});

var dibujar = function() {
    var lat_lng = new Array();
    var heatmap;
    var markers = [];
    if (!data.length) {
        alert('No hay clientes aún');
        window.close();
        return;
    }
    $.each(data, function(index, val) {
        var time = moment(val[3]);
        var myLatLng = new google.maps.LatLng(val[0], val[1]);
        lat_lng.push(myLatLng);
        
    });
    heatmap = new google.maps.visualization.HeatmapLayer({
      data: lat_lng,
      opacity: 1,
      map: map
        });
}

function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
}