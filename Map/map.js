var route=""
var bus_stop=""
var direction=""
var travel_time=420
$( "#submit" ).click(function() {
    route = $(".route").text()
    bus_stop= $(".route").text()
    direction=$(".direction").text()
    travel_time=$(".travel_time").text();
    if($("#map").length){
        $("#map").remove()
        }
    $( "body" ).append( $newdiv1, [ newdiv2, existingdiv1 ] );
})
 function initMap() {
            
            var busLatLng = {lat: 39.95, lng: -75.1667};

            var map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 100,
                  center: busLatLng
                });

            var bus_marker = new google.maps.Marker({
                  position: busLatLng,
                  map: map,
                  title: 'Your Location',
                  icon: 'img/bus_stop.png'
                    });   

            var flightPlanCoordinates = [
                {lat: 39.772, lng: -75.214},
                {lat: 39.291, lng: -75.821},
                {lat: 39.142, lng: -75.431},
                {lat: 39.467, lng: -75.027}
              ];
            var flightPath = new google.maps.Polyline({
                path: flightPlanCoordinates,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
              });

            flightPath.setMap(map);
        }