import csv
import json
import os
from flask import Flask, request, Response

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route('/api/breadcrumb', methods=['GET'])
def VehicleID_Start():
    vehicleId = request.args.get('vehicle', 'Anonymous')
    data = load_vehicle_data(vehicleId)
    if data:
        try:
            filename = f"{vehicleId}_filtered_data.json"
            response = Response(
                data,
                mimetype="application/json",
                headers={"Content-disposition":
                             f"attachment; filename={filename}"})
            return response
        except Exception as e:
            return f"Error occurred: {str(e)}"
    else:
        return "No data found"

def load_vehicle_data(vehicle_id):
    try:
        csv_file_path = 'samp.csv'
        stops_csv_file_path = 'stops.csv'
        
        vehicle_data = filter_csv_by_vehicle_id(csv_file_path, vehicle_id)
        vehicle_data_with_stops = load_stops_data(stops_csv_file_path, vehicle_id, vehicle_data)
        
        return json.dumps(vehicle_data_with_stops, indent=2)
    except FileNotFoundError:
        print("CSV file not found.")
        return []

def filter_csv_by_vehicle_id(csv_path, target_vehicle_id):
    filtered_data = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('VEHICLE_ID') == target_vehicle_id:
                filtered_data.append(row)
    return filtered_data

def load_stops_data(csv_path, target_vehicle_id, filtered_data):
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('VEHICLE_NUMBER').lstrip('0') == target_vehicle_id:
                filtered_data.append(row)
    return filtered_data

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)