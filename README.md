## The Paragraph
My database is for the Hotel Reservation Application. It has Guest, Rooms, Bookings and Reservation
Manager entity sets, where for a given entity in Guest there can be many entities in Rooms and
Bookings. However, for a given entity in Rooms and Bookings there can be at most one entity in Guest.
For a given entity in Bookings there must exist exactly one entity in Reservation Manager. However, for a
given entity in Reservation Manager there can be many entities in Bookings. Deleting an entity in Rooms
automatically deletes related entities in Bookings. Since all the FDs are key FDs, my tables satisfy Boyce-
Codd Normal Form.

## The Entity Relationship Diagram
 ![Tux, the Linux mascot](/assets/images/tux.png)

## Queries to retrieve information from the database
1. SELECT OfficeNumber, COUNT(*) AS manager_count FROM ReservationManager GROUP BY
OfficeNumber;
2. SELECT * FROM {table_name};
3. SELECT * FROM Guest WHERE Country = “Nigeria”;
4. SELECT Type, COUNT(*) AS num_rooms FROM Rooms GROUP BY Type;

#### Python Script: 
“HotelReservation.py.”

#### Populate Database Using Python:
“The HotelReservation.py reads the attached Guest.CSV file, Bookings.CSV file, Rooms.CSV file,
ReservationManager.CSV file and PriceTypes.CSV file to populate my tables.”

#### Printing the Data Using Python Chart Library:
“When HotelReservation.py is executed, it generates two bar charts representing the returned data from
query (1) & query (4) represented above.”
