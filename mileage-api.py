# Import
# Flask to create app object
# request to access request object
# jsonify to convert data to JSON
from flask import Flask, send_from_directory, request, jsonify
# Import os to access env vars
import os
# import load_dotenv to load env vars from .env
from dotenv import load_dotenv
## import the run_query function from sql.py
from sql import run_query
from flask_cors import CORS

# load env variables
load_dotenv()

# create an app object
app = Flask(__name__)
CORS(app)

# create a function to create our table
def create_table():
    # define the query as a string
    create_table_query = """
        CREATE TABLE IF NOT EXISTS trip(
        id SERIAL PRIMARY KEY,
        tripname VARCHAR NOT NULL,
        tripdate VARCHAR NOT NULL,
        startmileage INT NOT NULL,
        endmileage INT NOT NULL,
        costpermile FLOAT NOT NULL,
        reimbursement FLOAT NOT NULL
        );
        """

    # Run the create table query
    run_query(create_table_query)

# Run the create_table function
create_table()

@app.route('/')
def client():
    return send_from_directory('mileagetracker/src', 'index.html')


# create Route (CreateTrip)
@app.route('/trips', methods=['POST'])
def create_trip():
    #get the data from the rquest (json body)
    data = request.get_json()
    # write SQL query
    query = 'INSERT INTO trip (tripname, tripdate, startmileage, endmileage, costpermile, reimbursement) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;'

    # Run the query and get back results
    result = run_query(query, [data['tripname'], data['tripdate'], data['startmileage'], data['endmileage'], data['costpermile'], data['reimbursement']])
    # Return the ID to confirm it was created
    return jsonify({'id': result[0]['id']}), 201

# index Route
@app.route('/trips', methods=['GET'])
def get_trips():
    #Query String
    query = 'SELECT * FROM trip;'
    # Run the query and get back results
    results = run_query(query)
    # Turn the results into an array of dictionaries
    # Loop up list or dictionary comprehension
    results = [{'id': result['id'], 'tripname': result['tripname'], 'tripdate': result['tripdate'], 'startmileage': result['startmileage'], 'endmileage': result['endmileage'], 'costpermile': result['costpermile'], 'reimbursement': result['reimbursement']} for result in results]
    # Return the results as json
    return jsonify(results), 200

# SHOW ROUTE
@app.route('/trips/<int:trip_id>', methods=['GET'])
def show_trip(trip_id):
    query = 'SELECT * FROM trip WHERE id = %s;'
    result = run_query(query, [trip_id])
    if not result:
        return jsonify({'error': 'Trip not found'}), 404
    # COnvert result into dictionary (id, tripname, tripdate, startmileage, endmileage, costpermile)
    result = [{'id': result[0]['id'], 'tripname': result[0]['tripname'], 'tripdate': result[0]['tripdate'], 'startmileage': result[0]['startmileage'], 'endmileage': result[0]['endmileage'], 'costpermile': result[0]['costpermile'], 'reimbursement': result[0]['reimbursement']}]
    return jsonify(result) 

# Update route
@app.route('/trips/<int:trip_id>', methods=['PUT'])
def update_trip(trip_id):
    data = request.get_json()
    query = 'UPDATE trip SET tripname = %s, tripdate = %s, startmileage = %s, endmileage = %s, costpermile = %s, reimbursement = %s WHERE id = %s;' 
    run_query(query, [data['tripname'], data['tripdate'], data['startmileage'], data['endmileage'], data['costpermile'], data['reimbursement'], trip_id])
    return jsonify({'message': 'Trip updated successfully'})

# DELETE ROUTE
@app.route('/trips/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    query = 'DELETE FROM trip WHERE id = %s;'
    run_query(query, [trip_id])
    return jsonify({'message': 'Trip deleted successfully'})

# start the server
if __name__ == "__main__":
    
    app.run(debug=True, port=3000)
