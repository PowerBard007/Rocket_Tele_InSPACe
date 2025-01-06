import sqlite3
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Create a route to view data from the database
@app.route('/')
def home():
    return "Rocket Telemetry API is Running!"

# Insert telemetry data into the SQLite database
@app.route('/telemetry', methods=['POST'])
def receive_telemetry():
    data = request.json  # Get the data from the POST request

    # Extract data from the request with validation
    altitude = data.get('altitude')
    temperature = data.get('temperature')
    pressure = data.get('pressure')
    power = data.get('power')
    system_status = data.get('system_status')

    if altitude is None or temperature is None or pressure is None or power is None or system_status is None:
        return jsonify({"error": "Missing required data fields"}), 400

    # Connect to the database
    conn = sqlite3.connect('telemetry.db')
    c = conn.cursor()

    # Insert the telemetry data into the database with timestamp
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''INSERT INTO telemetry (altitude, temperature, pressure, power, system_status, timestamp)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
                 (altitude, temperature, pressure, power, system_status, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({"message": "Telemetry data received!", "data": data}), 201

# Retrieve all telemetry data from the database with optional filters
@app.route('/telemetry', methods=['GET'])
def get_telemetry():
    min_altitude = request.args.get('min_altitude', default=None, type=float)
    conn = sqlite3.connect('telemetry.db')
    c = conn.cursor()

    if min_altitude:
        c.execute('SELECT * FROM telemetry WHERE altitude >= ?', (min_altitude,))
    else:
        c.execute('SELECT * FROM telemetry')

    rows = c.fetchall()

    # Convert the data to JSON format
    telemetry_data = []
    for row in rows:
        telemetry_data.append({
            'id': row[0],
            'altitude': row[1],
            'temperature': row[2],
            'pressure': row[3],
            'power': row[4],
            'system_status': row[5],
            'timestamp': row[6]
        })

    conn.close()
    return jsonify(telemetry_data)

if __name__ == "__main__":
    app.run(debug=True)
