#!/usr/bin/env python3

### Due to VSCode default, do not run application in VSC terminal. Use py -m owmapp.main
### from system terminal.

import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
# Import environment variables at start for MySQL auth.
load_dotenv('dbconfig.env')

# Instantiates Flask application
app = Flask(__name__)

# Global variable for db connection
db_connector = None

# Attempt db connection on start
try:
    print("Attempting to import MySQLConnection...")
    from owmapp.database import MySQLConnection
    print("MySQLConnection imported successfully.")
    print("Attempting MySQL Authentication")
    
    # All of the code that uses MySQLConnection goes here
    db_connector = MySQLConnection(
        host_name="localhost",
        user_name=os.environ.get('DATABASEAUTH_USER'), # Assign value in dbconfig.env -- might need to create file in root directory
        user_password=os.environ.get('DATABASEAUTH_PASS'), # Assign value in dbconfig.env
        db_name="owmapp"
    )
    print("Connection object created.")

    if db_connector.connection and db_connector.connection.is_connected():
        print("Connection to database successful. Creating tables...")
        db_connector.create_tables()
        print("Tables created successfully!")
         
    else:
        print("Failed to connect to the database. Check credentials and server status.")

except ImportError as e:
    print(f"Error importing database module: {e}")
    sys.exit(1)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)

# Define endpoint for POST requests
@app.route('/weather_data', methods=['POST'])
def receive_weather_data():
    """This function handles incoming HTTP POST requests with a JSON payload."""
    if request.is_json:
        payload = request.get_json()
        print("Received payload: ", payload)
        # Pass JSON to DB logic
        try:
            return jsonify({"status": "success", "message": "Data received and stored"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "Request must be JSON"}), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
print()
print()
print()
print(f'Welcome to OWM app CLI interface. The goal is to create persistence of historical weather data.')


uinput = input("Define the zip code you wish to log : ")

while True:
    if uinput == 'q':
        db_connector.close()