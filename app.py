from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB (local instance for simplicity)
client = MongoClient("mongodb://localhost:27017/")  # Ensure MongoDB is running on port 27017
db = client['new_flight_db']  # New database name (replace 'flight_db')
routes_collection = db['routes']  # Collection name

# Dummy flight data with longitude and latitude for cities
dummy_data = [
    {
        "flight_id": "AI101",
        "departure": "New Delhi (DEL)",
        "destination": "New York City (JFK)",
        "airline": "Air India",
        "flight_type": "Direct",
        "departure_time": "2024-12-15T10:00:00",
        "arrival_time": "2024-12-15T14:00:00",
        "departure_coords": {"latitude": 28.6139, "longitude": 77.2090},  # New Delhi
        "destination_coords": {"latitude": 40.7128, "longitude": -74.0060}  # New York City
    },
    {
        "flight_id": "EK201",
        "departure": "New Delhi (DEL)",
        "destination": "New York City (JFK)",
        "airline": "Emirates",
        "flight_type": "Connecting",
        "connecting_airport": "Dubai (DXB)",
        "departure_time": "2024-12-16T02:00:00",
        "arrival_time": "2024-12-16T16:30:00",
        "connecting_time": "2024-12-16T06:30:00",
        "departure_coords": {"latitude": 28.6139, "longitude": 77.2090},  # New Delhi
        "destination_coords": {"latitude": 40.7128, "longitude": -74.0060},  # New York City
        "connecting_coords": {"latitude": 25.276987, "longitude": 55.296249}  # Dubai
    }
]

# Route to fetch dummy data for New Delhi to NYC flights
@app.route('/get-routes', methods=['GET'])
def get_routes():
    # Get the source and destination from the query parameters
    source = request.args.get('source', default='DEL', type=str).upper()  # Default is DEL (Delhi)
    destination = request.args.get('destination', default='JFK', type=str).upper()  # Default is JFK (NYC)

    # Clear the collection before inserting fresh data (Insert dummy data once)
    routes_collection.delete_many({})  # Remove existing routes
    routes_collection.insert_many(dummy_data)

    # Query routes based on source and destination
    routes = routes_collection.find({
        'departure': {'$regex': source, '$options': 'i'},  # Filter by source city (case-insensitive)
        'destination': {'$regex': destination, '$options': 'i'}  # Filter by destination city (case-insensitive)
    })

    # Prepare routes for JSON response
    routes_list = []
    for route in routes:
        route['_id'] = str(route['_id'])  # Convert ObjectId to string for JSON serialization
        routes_list.append(route)

    return jsonify({'routes': routes_list})

if __name__ == '__main__':
    app.run(debug=True)

