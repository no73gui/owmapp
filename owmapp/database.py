#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name,
                use_pure=True
            )
            if self.connection.is_connected():
                print(f"MySQL Database connection established!")
        except Error as err:
            print(f"Error: '{err}")


    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query Executed SUCCESSFULLY.")
        except Error as err:
            print(f"Error executing query: '{err}'")
            
    def create_tables(self):
        cursor = self.connection.cursor()
        
        create_zip_table = """CREATE TABLE IF NOT EXISTS
        zipCodes (zipCode VARCHAR(255) PRIMARY KEY
        )
        """
        cursor.execute(create_zip_table)
        
        create_weather_readings_table = """CREATE TABLE IF NOT EXISTS WeatherReadings (
        readingID INT AUTO_INCREMENT PRIMARY KEY,
        zipCode VARCHAR(255),
        temperature DECIMAL(5, 2),
        humidity DECIMAL(5, 2),
        wind_speed DECIMAL(5, 2),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (zipCode) REFERENCES zipCodes(zipCode)
        )
        """
        cursor.execute(create_weather_readings_table)# Create a separate table for severe weather events.
        create_severe_events_table = """CREATE TABLE IF NOT EXISTS SevereEvents (
        eventID INT AUTO_INCREMENT PRIMARY KEY,
        zipCode VARCHAR(255),
        event_type VARCHAR(255),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (zipCode) REFERENCES zipCodes(zipCode)
        )
        """
        cursor.execute(create_severe_events_table)

# This table stores data about the API calls themselves, for tracking purposes.
        create_api_logs_table = """CREATE TABLE IF NOT EXISTS ApiCallLogs (
        logID INT AUTO_INCREMENT PRIMARY KEY,
        zipCode VARCHAR(255),
        status_code INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (zipCode) REFERENCES zipCodes(zipCode)
        )
        """
        cursor.execute(create_api_logs_table)

# This table stores additional data from the API that you might not want to log every time.
        create_forecasts_table = """
        CREATE TABLE IF NOT EXISTS Forecasts (
        forecastID INT AUTO_INCREMENT PRIMARY KEY,
        zipCode VARCHAR(255),
        forecast_type VARCHAR(255),
        forecast_data JSON,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (zipCode) REFERENCES zipCodes(zipCode)
        )
        """
        cursor.execute(create_forecasts_table)
        # Commit the changes to the database
        self.connection.commit()

    def read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error reading query response: '{err}'")
            return None
        
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL Connection Closed")