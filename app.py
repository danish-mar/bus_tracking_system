# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import time
import uuid
import threading
import os

app = Flask(__name__)

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Load buses data or create empty file
BUSES_FILE = 'data/buses.json'
if os.path.exists(BUSES_FILE):
    with open(BUSES_FILE, 'r') as f:
        try:
            buses = json.load(f)
        except json.JSONDecodeError:
            buses = {}
else:
    buses = {}
    with open(BUSES_FILE, 'w') as f:
        json.dump(buses, f)

# Thread to check for inactive buses
def cleanup_inactive_buses():
    while True:
        current_time = time.time()
        inactive_buses = []
        
        for bus_id, bus_data in buses.items():
            last_update = bus_data.get('last_update', 0)
            if current_time - last_update > 10:  # 5 seconds timeout
                inactive_buses.append(bus_id)
        
        for bus_id in inactive_buses:
            print(f"Bus {bus_id} ({buses[bus_id]['name']}) timed out and was removed")
            buses.pop(bus_id, None)
        
        # Save updated buses data
        with open(BUSES_FILE, 'w') as f:
            json.dump(buses, f)
            
        time.sleep(1)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_inactive_buses, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bus')
def bus_device():
    return render_template('bus_device.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/api/register', methods=['POST'])
def register_bus():
    data = request.json
    bus_name = data.get('name', 'Unknown Bus')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not latitude or not longitude:
        return jsonify({'status': 'error', 'message': 'Location data required'}), 400
    
    # Generate a unique ID for the bus if not provided
    bus_id = data.get('bus_id', str(uuid.uuid4()))
    
    buses[bus_id] = {
        'name': bus_name,
        'latitude': latitude,
        'longitude': longitude,
        'last_update': time.time()
    }
    
    # Save updated buses data
    with open(BUSES_FILE, 'w') as f:
        json.dump(buses, f)
    
    return jsonify({'status': 'success', 'bus_id': bus_id})

@app.route('/api/update', methods=['POST'])
def update_location():
    data = request.json
    bus_id = data.get('bus_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if not bus_id or not latitude or not longitude:
        return jsonify({'status': 'error', 'message': 'Missing required data'}), 400
    
    if bus_id in buses:
        buses[bus_id]['latitude'] = latitude
        buses[bus_id]['longitude'] = longitude
        buses[bus_id]['last_update'] = time.time()
        
        # Save updated buses data
        with open(BUSES_FILE, 'w') as f:
            json.dump(buses, f)
        
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Bus not found'}), 404

@app.route('/api/buses', methods=['GET'])
def get_buses():
    return jsonify(buses)

@app.route('/api/bus/<bus_id>', methods=['GET'])
def get_bus(bus_id):
    if bus_id in buses:
        return jsonify(buses[bus_id])
    else:
        return jsonify({'status': 'error', 'message': 'Bus not found'}), 404

@app.route('/api/update_name', methods=['POST'])
def update_name():
    data = request.json
    bus_id = data.get('bus_id')
    new_name = data.get('name')
    
    if not bus_id or not new_name:
        return jsonify({'status': 'error', 'message': 'Missing required data'}), 400
    
    if bus_id in buses:
        buses[bus_id]['name'] = new_name
        
        # Save updated buses data
        with open(BUSES_FILE, 'w') as f:
            json.dump(buses, f)
        
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Bus not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)