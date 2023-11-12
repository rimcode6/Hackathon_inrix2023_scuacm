from flask import Flask, render_template, request
import json
from datetime import datetime
import pytz  # To handle time zones
import googlemaps  # You will need to install this package
import os  # For reading environment variables

app = Flask(__name__)

# Initialize Google Maps client with API key from environment variable
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyBEALSB8ogqVg-lr36gYfR-cFMRxZd3btc'))

@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have an 'index.html' template

@app.route('/get_stations', methods=['POST'])
def get_stations():
    user_location = request.form['location']

    try:
        with open('stations_data.json', 'r') as file:
            stations_data = json.load(file)

        if not isinstance(stations_data, list):
            return "JSON data format is incorrect - expected a list of objects"

        # Filter for stations in San Francisco
        sf_stations = [station for station in stations_data if station.get('city') == 'San Francisco']

        # Add additional information for each station
        for station in sf_stations:
            # Process each product for its type and price
            station['fuels'] = [{product['type']: product['price']} for product in station.get('products', [])]

            # Find the latest update date for calculating wait time
            latest_update = max(product['updateDate'] for product in station.get('products', [])) if station.get('products') else None
            station['wait_time'] = calculate_wait_time(latest_update)

            # Add Google Maps link
            station['google_maps_link'] = get_directions_link(user_location, station.get('address'))

        return render_template('stations.html', stations=sf_stations)
    except FileNotFoundError:
        return "JSON file not found"
    except json.JSONDecodeError:
        return "Error in reading the JSON file"

def calculate_wait_time(updateDate):
    if not updateDate:
        return None
    try:
        # Convert updateDate to a timezone-aware datetime object
        updateDate = datetime.fromisoformat(updateDate)
        updateDate = pytz.timezone('UTC').localize(updateDate)  # Assuming the updateDate is in UTC

        # Get the current time in the same timezone as updateDate
        current_time = datetime.now(pytz.timezone('America/Los_Angeles'))

        # Convert updateDate to the 'America/Los_Angeles' timezone
        updateDate_los_angeles = updateDate.astimezone(pytz.timezone('America/Los_Angeles'))


        # Calculate the wait time in minutes
        wait_time = current_time - updateDate_los_angeles
        return wait_time  # minutes

        # Calculate the wait time in seconds
        wait_time = current_time - updateDate_los_angeles
        return wait_time.total_seconds()  # Convert to total seconds
    
    except ValueError:
        return None

def get_directions_link(user_location, station_address):
    if not user_location or not station_address:
        return None
    try:
        # Construct the Google Maps URL for directions
        return f"https://www.google.com/maps/dir/?api=1&origin={user_location}&destination={station_address}"
    except Exception as e:
        print(f"Error getting directions: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
