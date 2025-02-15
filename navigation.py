<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route Navigation</title>
    <style>
        /* Basic Styling */
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            text-align: center;
        }
        h1 {
            margin-top: 20px;
            color: #2a9d8f;
        }
        .map-container {
            height: 80vh;
            width: 100%;
            margin-top: 20px;
        }
        .button-container {
            margin-top: 20px;
        }
        .button {
            background-color: #264653;
            color: white;
            padding: 15px 30px;
            font-size: 1.2em;
            border: none;
            cursor: pointer;
            border-radius: 10px;
            transition: 0.3s;
        }
        .button:hover {
            background-color: #e76f51;
        }
    </style>
</head>
<body>

    <h1>Route Navigation</h1>

    <div class="map-container" id="map"></div>

    <div class="button-container">
        <button class="button" onclick="getDirections()">Get Directions</button>
    </div>

    <script>
        // Initialize the Google Maps API
        let map;
        let directionsService;
        let directionsRenderer;

        function initMap() {
            // Initialize map with a default location (e.g., San Francisco)
            map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: 37.7749, lng: -122.4194 },
                zoom: 12,
            });

            directionsService = new google.maps.DirectionsService();
            directionsRenderer = new google.maps.DirectionsRenderer();
            directionsRenderer.setMap(map);
        }

        // Get directions from a start point to a destination
        function getDirections() {
            const request = {
                origin: 'San Francisco, CA', // Set origin
                destination: 'Los Angeles, CA', // Set destination
                travelMode: google.maps.TravelMode.DRIVING, // Mode of transportation
            };

            directionsService.route(request, function (result, status) {
                if (status === google.maps.DirectionsStatus.OK) {
                    directionsRenderer.setDirections(result);
                } else {
                    alert('Directions request failed due to ' + status);
                }
            });
        }

        // Load Google Maps API asynchronously
        function loadScript() {
            const script = document.createElement('script');
            script.src = 'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap';
            script.async = true;
            document.head.appendChild(script);
        }

        // Call the function to load Google Maps
        loadScript();
    </script>

</body>
</html>
