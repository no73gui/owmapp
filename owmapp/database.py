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
        
        # This is the correct SQL statement for the StorageLocation table
        create_storage_table = """CREATE TABLE IF NOT EXISTS
        StorageLocation (storageArea VARCHAR(255) PRIMARY KEY
        )
        """
        cursor.execute(create_storage_table)

        # Added the table name 'Consumables' and corrected the foreign key reference
        create_consumables_table = """CREATE TABLE IF NOT EXISTS Consumables (
        consumableID INT AUTO_INCREMENT PRIMARY KEY,
        storageArea VARCHAR(255),
        FOREIGN KEY (storageArea) REFERENCES StorageLocation(storageArea)
        )
        """
        cursor.execute(create_consumables_table)

        # Added the table name 'Tools' and corrected the foreign key reference
        create_tools_table = """CREATE TABLE IF NOT EXISTS Tools (
        toolID INT AUTO_INCREMENT PRIMARY KEY,
        storageArea VARCHAR(255),
        FOREIGN KEY (storageArea) REFERENCES StorageLocation(storageArea)
        )
        """
        cursor.execute(create_tools_table)
        
        # This table must be created before Employee_Tools and Employee_Consumables
        create_employee_table = """CREATE TABLE IF NOT EXISTS Employee (
        employeeID INT AUTO_INCREMENT PRIMARY KEY
        )
        """
        cursor.execute(create_employee_table)

        # Corrected the foreign key syntax and made sure it's called after the employee and tools tables are created
        create_employee_tools_table = """CREATE TABLE IF NOT EXISTS Employee_Tools (
        employeeID INT,
        toolID INT,
        PRIMARY KEY (employeeID, toolID),
        FOREIGN KEY (employeeID) REFERENCES Employee(employeeID),
        FOREIGN KEY (toolID) REFERENCES Tools(toolID)
        )
        """
        cursor.execute(create_employee_tools_table)

        # Corrected the foreign key syntax and reference
        create_employee_consumables_table = """
        CREATE TABLE IF NOT EXISTS Employee_Consumables (
        employeeID INT,
        consumableID INT,
        PRIMARY KEY (employeeID, consumableID),
        FOREIGN KEY (employeeID) REFERENCES Employee(employeeID),
        FOREIGN KEY (consumableID) REFERENCES Consumables(consumableID)
        )
        """
        cursor.execute(create_employee_consumables_table)

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