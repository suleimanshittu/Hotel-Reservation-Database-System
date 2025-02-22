import mysql.connector
from mysql.connector import Error
import csv
import plotly.graph_objects as go
import plotly.io as pio  # Import plotly.io to control the renderer

# Set the default renderer to 'browser' to avoid using kaleido
pio.renderers.default = "browser"  # This ensures the plot is shown in the browser

def create_mysql_connection(host_name, user_name, user_password):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        if connection.is_connected():
            print("Connected to MySQL")
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def create_database(connection, db_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")

        
#########################################################################################

def create_Guest_table(connection, db_name):

    try:
        connection.database = db_name  # Switch to the target database
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Guest (
            Guest_ID VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,
            FullName TEXT,
            EmailAddress VARCHAR(30),
            PhoneNumber VARCHAR(25),
            Country TEXT,
            ArrivalDate DATE,
            DepartureDate DATE
        )
        """
        cursor.execute(create_table_query)
        print("Table 'Guest' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")
        
##########################################################################################

def create_Rooms_table(connection, db_name):

    try:
        connection.database = db_name  # Switch to the target database
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Rooms (
            RoomNumber INTEGER PRIMARY KEY NOT NULL UNIQUE,
            Type VARCHAR(15),
            Availability BOOLEAN,
            Guest_ID VARCHAR(3),
            FOREIGN KEY(Guest_ID) REFERENCES Guest(Guest_ID) ON DELETE SET NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table 'Rooms' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")


########################################################################################## --normalised table - PriceTypes
def create_PriceTypes_table(connection, db_name):

    try:
        connection.database = db_name  # Switch to the target database
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS PriceTypes (
            Type VARCHAR(15),
            Price DECIMAL(10,2),
            PRIMARY KEY(Type)
        )
        """
        cursor.execute(create_table_query)
        print("Table 'PriceTypes' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")


##########################################################################################

def create_Bookings_table(connection, db_name):

    try:
        connection.database = db_name  # Switch to the target database
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Bookings (
            Booking_ID VARCHAR(4) NOT NULL UNIQUE,
            Guest_ID VARCHAR(3),
            RoomNumber INTEGER NOT NULL UNIQUE,
            BookingDate DATE,
            Manager_ID VARCHAR(3) NOT NULL,
            PRIMARY KEY(Booking_ID, RoomNumber),
            FOREIGN KEY(Guest_ID) REFERENCES Guest(Guest_ID) ON DELETE SET NULL,
            FOREIGN KEY(RoomNumber) REFERENCES Rooms(RoomNumber) ON DELETE CASCADE,
            FOREIGN KEY(Manager_ID) REFERENCES ReservationManager(Manager_ID) ON DELETE CASCADE
        )
        """
        cursor.execute(create_table_query)
        print("Table 'Bookings' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")
        
###################################################################################

def create_ReservationManager_table(connection, db_name):

    try:
        connection.database = db_name  # Switch to the target database
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ReservationManager (
            Manager_ID VARCHAR(3) PRIMARY KEY,
            OfficeNumber INTEGER,
            Name TEXT,
            Gender TEXT,
            DOB DATE
        )
        """
        cursor.execute(create_table_query)
        print("Table 'ReservationManager' created successfully or already exists.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")
                


def populate_multiple_tables_from_csv(connection, csv_file_path, table_name):  

    try:
        cursor = connection.cursor()
        
        if table_name == "Guest":
            insert_query = """
                INSERT INTO Guest (Guest_ID, FullName, EmailAddress, PhoneNumber, Country, ArrivalDate, DepartureDate) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE FullName = VALUES(FullName),
                EmailAddress = VALUES(EmailAddress),
                PhoneNumber = VALUES(PhoneNumber),
                Country = VALUES(Country),
                ArrivalDate = VALUES(ArrivalDate),
                DepartureDate = VALUES(DepartureDate);
                """
        elif table_name == "Rooms":
                insert_query = """
                INSERT INTO Rooms (RoomNumber, Type, Availability)
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE RoomNumber = VALUES(RoomNumber);
                """
        elif table_name == "PriceTypes":
                insert_query = """
                INSERT INTO PriceTypes (Type, Price)
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE Type = VALUES(Type);
                """
        elif table_name == "Bookings":
                insert_query = """
                INSERT INTO Bookings (Booking_ID, Guest_ID, RoomNumber, BookingDate, Manager_ID)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Booking_ID = VALUES(Booking_ID);
                """
        elif table_name == "ReservationManager":
                insert_query = """
                INSERT INTO ReservationManager (Manager_ID, OfficeNumber, Name, Gender, DOB)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Manager_ID = VALUES(Manager_ID);
                """
        else:
            print("INVALID TABLE NAME")
            return
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                cursor.execute(insert_query, row)
        
        connection.commit()
        print("Data from CSV inserted successfully into all the tables.")
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")



def print_table_content(connection, table_name, csv_file_path):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print(f"Table '{table_name}' content:")
        for row in rows:
            print(row)
       
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")
        

def print_guest_content_for_nigeria(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Guest WHERE Country = 'Nigeria'")
        rows = cursor.fetchall()

        print("Guest Content for Nigeria:")
        for row in rows:
            print(row)
       
        cursor.close()
    except Error as e:
        print(f"Error: '{e}'")        
        
def query_and_plot_bar(connection):
    """Queries RoomNumber and count of bookings from Bookings and displays a bar chart."""
    cursor = connection.cursor()
    retrieve_query = """ SELECT Type, COUNT(*) AS num_rooms FROM Rooms GROUP BY Type; """
    cursor.execute(retrieve_query)
    
    # Fetch all rows of the query s
    data = cursor.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the Bookings table. Exiting.")
        return

    # Extract the values
    Type = [row[0] for row in data]
    Room_number = [row[1] for row in data]
          
    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=Type,
            y=Room_number,
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Number of Rooms per Room Type",
        xaxis_title="RoomTypes",
        yaxis_title="No of Rooms",
        template="plotly_dark"
    )
    
    # Display the bar chart in a web browser (default renderer)
    bar_chart.show()
    
        
    
###########################################################################################

def query_and_plot_bar2(connection):
    """Queries OfficeNumber and count of Managers from ReservationManager and displays a bar chart."""
    cursor = connection.cursor()
    retrieve_query = """ SELECT OfficeNumber, COUNT(*) AS manager_count FROM ReservationManager GROUP BY OfficeNumber; """
    cursor.execute(retrieve_query)
    
    # Fetch all rows of the query results
    data = cursor.fetchall()

    # Check if data is None or empty
    if data is None or len(data) == 0:
        print("No data found in the Bookings table. Exiting.")
        return

    # Extract the values
    Office_number = [row[0] for row in data]
    ManagerCount = [row[1] for row in data]
          
    # Create a bar chart using Plotly
    bar_chart = go.Figure(data=[
        go.Bar(
            x=Office_number,
            y=ManagerCount,
            textposition='auto',
            marker=dict(color='royalblue')
        )
    ])
    
    # Update layout for better appearance
    bar_chart.update_layout(
        title="Number of Managers per Office",
        xaxis_title="Office Numbers",
        yaxis_title="No of Managers",
        template="plotly_dark"
    )
    
    # Display the bar chart in a web browser (default renderer)
    bar_chart.show()

if __name__ == "__main__":
    connection = create_mysql_connection('','','')
    if connection:
        create_database(connection, "HOTELRESERVATION")
        create_Guest_table(connection, "HOTELRESERVATION")
        create_Rooms_table(connection, "HOTELRESERVATION")
        create_PriceTypes_table(connection, "HOTELRESERVATION")
        create_ReservationManager_table(connection, "HOTELRESERVATION")
        create_Bookings_table(connection, "HOTELRESERVATION")
        
            
        populate_multiple_tables_from_csv(connection, "Guest.csv", "Guest")
        populate_multiple_tables_from_csv(connection, "ReservationManager.csv", "ReservationManager")
        populate_multiple_tables_from_csv(connection, "Rooms.csv", "Rooms")
        populate_multiple_tables_from_csv(connection, "PriceTypes.csv", "PriceTypes")
        populate_multiple_tables_from_csv(connection, "Bookings.csv", "Bookings")
  
        print_table_content(connection, "Guest", "Guest.csv")
        print_table_content(connection, "ReservationManager", "ReservationManager.csv")
        print_table_content(connection, "Rooms", "Rooms.csv")
        print_table_content(connection, "PriceTypes", "PriceTypes.csv")
        print_table_content(connection, "Bookings", "Bookings.csv")
        
        print_guest_content_for_nigeria(connection)
        
        query_and_plot_bar(connection)
        query_and_plot_bar2(connection)
        
        connection.close()
    else:
        print("Failed to connect to MySQL")
    
