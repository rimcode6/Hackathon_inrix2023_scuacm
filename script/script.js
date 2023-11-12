document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const locationInput = document.getElementById('location');
    const currentLocationBtn = document.getElementById('current-location');
    const mapFrame = document.getElementById('map').querySelector('iframe');

    function updateMap(location) {
        const encodedLocation = encodeURIComponent(location);
        mapFrame.src = `https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q=${encodedLocation}`;
    }

    function fetchCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const { latitude, longitude } = position.coords;
                const locationString = `${latitude}, ${longitude}`;
                locationInput.value = locationString;
                updateMap(locationString);
            }, () => {
                alert('Error: Unable to fetch your current location.');
            });
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const location = locationInput.value;
        if (location) {
            updateMap(location);
        }
    });

    currentLocationBtn.addEventListener('click', function(event) {
        fetchCurrentLocation();
    });

    // Initialize map with default location
    updateMap('San Francisco');
});
