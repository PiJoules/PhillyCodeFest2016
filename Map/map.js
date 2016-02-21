var route="";
var bus_stop="";
var direction="";
var travel_time=420;
var map;
$( "#submit" ).click(function() {
    route = $(".route").text();
    bus_stop= $(".stop").text();
    direction=$(".direction").text();
    travel_time=parseInt($(".travel_time").text())*60;
    $( "body" ).append( "<div class=' text-center' id='map' style='height: 80%'></div>" );
    var route_url = "http://144.118.98.89:8080/stops/"+route;
    var RouteCoordinates =[];
    var BusCoordinates = [];
    var MainStop;
    $.getJSON(route_url, function(data) 
            {
                $.each(data, function(row)
                {
                    RouteCoordinates.push({lat: row["lat"], lng: row["lng"]});
                    if (row["stopid"] == bus_stop)
                    {
                        MainStop={lat: row["lat"], lng: row["lng"]};
                    }
                });
                
            }); 
    
//    var bus_url = "http://www3.septa.org/hackathon/TransitView/"+route;
    var bus_url = "http://144.118.98.89:8080/transitview/" + route;
    $.getJSON(bus_url, function(data) 
            {
                $.each(data, function(row) 
                {
                    BusCoordinates.push({lat: row["lat"], lng: row["lng"], id: row["label"] });
                    });
                
            }); 
            
    var nearest_bus_url = "http://144.118.98.89:8080/data_test" //?route=" + route + "&direction=" + direction + "&stop_id=" + bus_stop + "&user_offset=" + travel_time;
    var eta;
    $.getJSON(nearest_bus_url, function(data) 
            {
                eta = data["eta"]; 
                $.each(BusCoordinates, function(row){
                   if(row["label"] === data["nearest_bus"]["label"])
                   {
                       row["lat"] = data["nearest_bus"]["lat"];
                       row["lng"] = data["nearest_bus"]["lng"];
                   }
                });
                
            }); 
    var routePath = new google.maps.Polyline({
                path: RouteCoordinates,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
              });

            routePath.setMap(map);

    $.each(BusCoordinates, function(row){
    var bus_marker = new google.maps.Marker({
        position: {lat: row["lat"], lng: row["lng"]},
        map: map,
        title: 'Your Location',
        icon: 'img/bus_stop.png'
          });   

               });
     var stop_marker = google.maps.Marker({
        position: MainStop,
        map: map,
        title: 'Your Location',
        icon: 'img/bus_stop.png'
          });   

               });

 function initMap() {
            
     
            var LatLng = {lat: 39.95, lng: -75.1667};

            map = new google.maps.Map(document.getElementById('map'), {
                  zoom: 100,
                  center: LatLng
                });

            
        }