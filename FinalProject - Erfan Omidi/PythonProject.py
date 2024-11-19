import mysql.connector
from mysql.connector import Error
import os

# Database connection
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




# Checking a single query with data
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        
        
# Function to append data to the reservation file
def append_to_dreservation_file(file_path, data):
    # Check if the file ends with a newline
    try:
        with open(file_path, 'rb+') as file:
            file.seek(-1, os.SEEK_END)
            if file.read(1) != b'\n':
                file.write(b'\n')  # Add a newline 
    except FileNotFoundError:
        pass  

    # Append the new data
    with open(file_path, 'a') as file:
        file.write(data + '\n')



def prompt_for_customer_info():
    first_name = input("Enter customer's first name: ")
    last_name = input("Enter customer's last name: ")
    email = input("Enter customer's email: ")
    phone_number = input("Enter customer's phone number: ")
    return first_name, last_name, email, phone_number







# Check-in 
def check_in(connection):
    first_name, last_name, email, phone_number = prompt_for_customer_info()
    cursor = connection.cursor(buffered=True)
    cursor.execute("SELECT id, room_type FROM inn_rooms WHERE availability > 0 ORDER BY room_type")
    available_rooms = cursor.fetchall()
    if not available_rooms:
        print("No available rooms. Check-in process cannot be completed.")
        return

    for room in available_rooms:
        print(f"Room ID: {room[0]}, Room Type: {room[1]}")
    
    room_id = input("Enter the Room ID for check-in: ")
    accommodation_days = input("Enter the number of days for accommodation: ")

    # Insert customer details into inn_customer table
    insert_customer_query = "INSERT INTO inn_customer (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)"
    execute_query(connection, insert_customer_query, (first_name, last_name, email, phone_number))
    customer_id = cursor.lastrowid

    # Insert reservation into inn_reservation table
    insert_reservation_query = "INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, checkout) VALUES (%s, %s, %s, 0)"
    execute_query(connection, insert_reservation_query, (room_id, customer_id, accommodation_days))

    # Decrease the availability of the chosen room
    update_room_availability_query = "UPDATE inn_rooms SET availability = availability - 1 WHERE id = %s"
    execute_query(connection, update_room_availability_query, (room_id,))

    # Append data to reservation file
    reservation_data = f"{first_name},{last_name},{email},{phone_number},{room_id},{accommodation_days}"
    file_path = "R:\\s3\\python\\FinalProject\\dreservation_file.txt"
    append_to_dreservation_file(file_path, reservation_data)

    print(f"Reservation for {first_name} {last_name} added to the reservation file.")
    
    
    
    
    
# Check-out
def check_out(connection):
    phone_number = input("Please give your phone number: ")
    print(f"Looking up reservations for phone number: {phone_number}")  # Debugging 

    cursor = connection.cursor(buffered=True)
    try:
        # Find reservation with phone number
        cursor.execute("""
        SELECT r.id, c.first_name, c.last_name, r.accommodation_days, r.cost
        FROM inn_reservation r
        JOIN inn_customer c ON r.customer_id = c.id
        WHERE c.phone_number = %s AND r.checkout = 0
        """, (phone_number,))
        reservation = cursor.fetchone()

         
        print(f"Reservation data retrieved: {reservation}")

        if reservation:
            print("Checkout in progress ...")
            reservation_id, first_name, last_name, days, cost = reservation
            print(f"Your invoice information is:\nName: {first_name} {last_name}\nAccommodation: {days} days\nTotal Cost: {cost} $")

            # Update reservation as checked-out
            update_reservation_query = "UPDATE inn_reservation SET checkout = 1 WHERE id = %s"
            execute_query(connection, update_reservation_query, (reservation_id,))

            # Increase room availability
            update_room_availability_query = """
            UPDATE inn_rooms r
            JOIN inn_reservation res ON r.id = res.room_type
            SET r.availability = r.availability + 1
            WHERE res.id = %s
            """
            execute_query(connection, update_room_availability_query, (reservation_id,))
            print("Check-out successful. Thank you and see you next time!")
        else:
            print("No reservation found for the given phone number.")
    except Error as err:
        print(f"An error occurred: {err}")

        
        

#---------------------------------------------------------------------------------------------------------------main---------------------------------------------------------------------------------------------#

# Console function
def interactive_console(connection):
    while True:
        print("*******************Welcome to the LIRS system*******************")
        print("Please enter a number related to the following option to continue:")
        print("Check-out: 1")
        print("Check-in: 2")
        print("Exit: 0")
        choice = input("Your option: ")
        
        if choice == '1':
            check_out(connection)
        elif choice == '2':
            check_in(connection)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")
            
            

# Txt file
def read_file_and_update_db(connection, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            
            first_name, last_name, email, phone_number, room_type, accommodation_days = line.strip().split(',')
            phone_number = int(phone_number)  # string to integer
            accommodation_days = int(accommodation_days)  

            # Find or create customer and get customer_id
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT id FROM inn_customer WHERE phone_number = %s", (phone_number,))
            customer_result = cursor.fetchone()
            if customer_result:
                customer_id = customer_result[0]
            else:
                cursor.execute("""
                    INSERT INTO inn_customer (first_name, last_name, email, phone_number)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, email, phone_number))
                connection.commit()
                customer_id = cursor.lastrowid

            # Insert reservation info
            cursor.execute("""
                INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, checkout)
                VALUES ((SELECT id FROM inn_rooms WHERE room_type = %s), %s, %s, 0)
            """, (room_type, customer_id, accommodation_days))
            connection.commit()

            print(f"Added reservation for {first_name} {last_name}")

            

def main():
    # Connect 
    connection = create_db_connection("localhost", "erffn", "2306562", "Inn_reservation")
    
    # Path 
    file_path = "R:\s3\python\FinalProject\dreservation_file.txt"

    # If the reservation file exists 
    if os.path.exists(file_path):
        read_file_and_update_db(connection, file_path)
    else:
        print("Reservation file not found, moving to interactive mode.")

   
    interactive_console(connection)

if __name__ == "__main__":
    main()