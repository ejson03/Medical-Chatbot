var map1, map2;

function initMap (){
    if (navigator.geolocation) {
        try {
            navigator.geolocation.getCurrentPosition(async function(position) {
                var myLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                await setPos(myLocation);
            },
            function(error){
            switch(error.code){
                    case 1:
                        alert("Please enable geolocation permission in your browser settings to view this page");
                        break;
                    case 2:
                        alert("There seems to be a problem getting the location. Check if GPS is enabled");
                        break;
                    case 3:
                        alert("Getting your location timed out. Please try again.");
                        break;        
                }
                console.log(error.message);            
            });
            //
        } catch (err) {
            var myLocation = {
            lat: 23.8701334,
            lng: 90.2713944
            };
            setPos(myLocation);
        }
    } else {
    var myLocation = {
        lat: 23.8701334,
        lng: 90.2713944
    };
    setPos(myLocation);
    }
    
}

function setPos(myLocation) {
    map1 = new google.maps.Map(document.getElementById('map1'), {
        center: myLocation,
        zoom: 10
    });
    map2 = new google.maps.Map(document.getElementById('map2'), {
        center: myLocation,
        zoom: 10
    });
    console.log(map1, map2)
    var service = new google.maps.places.PlacesService(map1);
    service.nearbySearch({
        location: myLocation,
        radius: 4000,
        types: ['hospital']
    }, processResults1);

    var service = new google.maps.places.PlacesService(map2);
    service.nearbySearch({
        location: myLocation,
        radius: 4000,
        types: ['hospital']
    }, processResults2);

}

function processResults1(results, status, pagination) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return;
    } else {
        createMarkers(results, map1);

    }
}

function processResults2(results, status, pagination) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return;
    } else {
        createMarkers(results, map2);

    }
}

function createMarkers(places, map) {
    var bounds = new google.maps.LatLngBounds();

    for (var i = 0, place; place = places[i]; i++) {
        console.log(places[i])
        var image = {
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(20, 20)
        };

        var marker = new google.maps.Marker({
            map: map,
            icon: image,
            title: place.name,
            animation: google.maps.Animation.DROP,
            position: place.geometry.location
        });
        
        addInfoWindow(map, marker, place.name, place.vicinity, place.rating)

        bounds.extend(place.geometry.location);
    }
    map.fitBounds(bounds);
}

function addInfoWindow(map, marker, place, address, rating) {

    var infoWindow = new google.maps.InfoWindow({
        content: makeContent(place, address, rating)
    });
    google.maps.event.addListener(marker, 'mouseover', function () {
        infoWindow.open(map, marker);
    });
    google.maps.event.addListener(marker, 'mouseout', function () {
        infoWindow.close();
    });
    google.maps.event.addListener(marker, 'click', async function () {
        url = await getURL(place, address);
        window.open(url, '_blank');
    });
}

function makeContent(place, address, rating){
    var contentString = `<div id="content"> 
    <div id="siteNotice">
    </div>
    <h5 id="firstHeading" class="firstHeading">${place}</h1>
    <div id="bodyContent">
    <p><bold>Address<bold> : ${address} <p>
    <p><bold>Rating<bold> : ${rating} <p>
    </div>
    </div>`

    return contentString;
}

async function getURL(place, address){     
    let response = await fetch(`/website/${place}`);
    let users = await response.json();
    console.log(users['url']);
    return users['url']

}