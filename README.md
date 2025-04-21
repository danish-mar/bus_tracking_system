# Bus Tracking System

A simple Flask-based real-time bus tracking system with two modules:

1. **Bus Device Module**: Simulates ESP32 devices on buses, sending location updates every second
2. **Map View Module**: Shows all active buses on a real-time map

## Features

- Real-time location tracking using browser geolocation API
- Automatic removal of inactive buses (no updates for 5 seconds)
- Custom bus names that can be updated on the fly
- Live map showing all active buses
- Responsive design that works on both desktop and mobile devices
- Light green theme with Bootstrap and Tailwind CSS styling

## Requirements

- Python 3.6+
- Flask
- Internet connection (for loading maps and libraries)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bus-tracking-system.git
   cd bus-tracking-system
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install flask
   ```

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. The main page will show two options:
   - Bus Device: Use this on the device you want to act as a bus
   - Map View: Use this to monitor all buses

## Using the System

### Bus Device Module

1. Enter a bus name
2. Click "Request Location Permission & Start Tracking"
3. Allow location access when prompted
4. The device will now send location updates every second
5. You can update the bus name at any time using the provided form

### Map View Module

1. All active buses will appear on the map and in the list
2. The map refreshes every second
3. Click on a bus in the list to center the map on it
4. Buses that don't send updates for 5 seconds are automatically removed

## Project Structure

```
bus-tracking-system/
├── app.py                  # Main Flask application
├── data/
│   └── buses.json          # Bus data storage (created automatically)
└── templates/
    ├── index.html          # Main page
    ├── bus_device.html     # Bus device interface
    └── map.html            # Map view interface
```

## Libraries Used

- Flask: Backend web framework
- Leaflet.js: Interactive maps
- Bootstrap: UI components and responsive design
- Font Awesome: Icons
- Tailwind CSS: Additional styling

## Notes

- This system uses browser geolocation, which requires HTTPS in production
- For development purposes, it works on HTTP localhost
- The system stores bus data in a JSON file; for production use, consider using a database
- Location updates are sent every second, which may affect battery life on mobile devices