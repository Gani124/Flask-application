import csv, json
import os
from flask import Flask, jsonify, request, Response

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
        filtered_data = filter_csv_by_vehicle_id(csv_file_path, vehicle_id)
        return json.dumps(filtered_data, indent=2)
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

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)
#=================================================================================================
import csv
import json
import os
from flask import Flask, Response, request

app = Flask(__name__)
wsgi_app = app.wsgi_app

@app.route('/api/breadcrumb', methods=['GET'])
def vehicle_id_start():
    vehicle_id = request.args.get('vehicle', 'Anonymous')
    try:
        csv_file_path = 'samp.csv'
        filtered_data = filter_csv_by_vehicle_id(csv_file_path, vehicle_id)
        
        if filtered_data:
            filename = f"{vehicle_id}_filtered_data.json"
            with open(filename, 'w') as json_file:
                json.dump(filtered_data, json_file, indent=2)

            with open(filename, 'r') as json_file:
                response = Response(
                    json_file.read(),
                    mimetype="application/json",
                    headers={"Content-disposition": f"attachment; filename={filename}"}
                )
                return response
        else:
            return "No data found"
    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def filter_csv_by_vehicle_id(csv_path, target_vehicle_id):
    filtered_data = []
    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('VEHICLE_ID') == target_vehicle_id:
                filtered_data.append(row)
    return filtered_data

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)

