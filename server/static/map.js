var route="";
var bus_stop="";
var direction="";
var travel_time=420;
var map;
$( "#submit" ).click(function() {
    console.log("text");
    route = $(".route").val();
    bus_stop= $(".stop").val();
    direction=$(".direction").val();
    console.log("some", route, direction, bus_stop);
    travel_time=parseInt($(".travel_time").text())*60;
    // $( "body" ).append( "<div class=' text-center' id='map' style='height: 80%'></div>" );
    var route_url = "/stops/"+route;
    var RouteCoordinates =[];
    var BusCoordinates = [];
    var MainStop;
    $.getJSON(route_url, function(data) {
        $.each(data, function(row, elem){
            RouteCoordinates.push({lat: elem["lat"], lng: elem["lng"]});
            // console.log(elem["stopid"] + "", bus_stop, (elem["stopid"] + "") == bus_stop);
            if ((elem["stopid"] + "") == bus_stop)
            {
                MainStop={lat: elem["lat"], lng: elem["lng"]};

                var bus_url = "/transitview/" + route;
                // console.log(MainStop);
                $.getJSON(bus_url, function(data) {
                    $.each(data["bus"], function(index, row) {
                        // console.log(row);
                        BusCoordinates.push({lat: row["lat"], lng: row["lng"], id: row["label"] });

                        var nearest_bus_url = "/data_test";
                        //?route=" + route + "&direction=" + direction + "&stop_id=" + bus_stop + "&user_offset=" + travel_time;
                        // var nearest_bus_url = "/data?route=" + route + "&direction=" + direction + "&stop_id=" + bus_stop + "&user_offset=" + travel_time;
                        var eta;
                        // console.log(BusCoordinates);
                        $.getJSON(nearest_bus_url, function(data) {
                            eta = data["eta"]; 
                            $.each(BusCoordinates, function(index, busCoord){
                               if(busCoord["label"] === data["nearest_bus"]["label"])
                               {
                                   busCoord["lat"] = parseFloat(data["nearest_bus"]["lat"]);
                                   busCoord["lng"] = parseFloat(data["nearest_bus"]["lng"]);
                               }

                                // var routePath = new google.maps.Polyline({
                                    // path: RouteCoordinates,
                                    // geodesic: true,
                                  //   strokeColor: '#FF0000',
                                  //   strokeOpacity: 1.0,
                                  //   strokeWeight: 2
                                  // });

                                // routePath.setMap(map);

                                $.each(BusCoordinates, function(index, busCoord2){
                                    var bus_marker = new google.maps.Marker({
                                        position: {lat: parseFloat(busCoord2["lat"]), lng: parseFloat(busCoord2["lng"])},
                                        map: map,
                                    });   
                                });
                                var stop_marker = new google.maps.Marker({
                                    position: MainStop,
                                    map: map,

                                    title: 'Your Location',
                                    icon: '/static/img/bus_stop.png'
                                });
                                map.setCenter(MainStop);
                            });
                            
                        }); 
                    });
                            
                }); 
            }
        });        
    });  
});

 function initMap() {
            
     
            var LatLng = {lat: 39.95, lng: -75.1667};

            map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 15,
                  center: LatLng
                });

            
        }