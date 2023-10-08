# Import
# Flask to create app object
# request to access request object
# jsonify to convert data to JSON
from flask import Flask, request, jsonify
# Import os to access env vars
import os
# import load_dotenv to load env vars from .env
from dotenv import load_dotenv
## import the run_query function from sql.py
from sql import run_query

# load env variables
load_dotenv()

# create an app object
app = Flask(__name__)

# create a function to create our table
def create_table():
    # define the query as a string
    create_table_query = """
        CREATE TABLE OF NOT EXISTS trip (
        id SERIAL PRIMARY KEY,
        tripname VARCHAR NOT NULL,
        tripdate VARCHAR NOT NULL,
        startmileage INT NOT NULL,
        endmileage INT NOT NULL,
        costpermile FLOAT NOT NULL
    );
    """

    # Run the create teable query
    run_query(create_table_query)

# Run the create_table function
create_table()

# create Route (CreateTrip)
@app.route('/trips', methods=['POST'])
def create_trip():
    #get teh data from the rquest (json body)
    data = request.get_json()
    # write SQL query
    query = 'INSERT INTO trip (tripname, tripdate, startmileage, endmileage, costpermile) VALUES (%s, %s, %s, %s, %s) RETURNING id;'

    # Runt he query and get back results
    result = run_query(query, [data['tripname'], data["tripdate"], data["startmileage"], data["endmileage"], data["costpermile"]])
    # Return the ID to confirm it was created
    return jsonify({"id": result[0]["id"]}), 201

