import mysql.connector
from mysql.connector import Error

# Change these values if your MySQL login is different.
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
DB_NAME = "ticket_booking"


def connect_server():
    """Connect to MySQL server without selecting a database."""
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Error as error:
        print("MySQL server connection failed:", error)
        return None


def setup_database():
    """Create the database and tables if they do not already exist."""
    connection = connect_server()
    if not connection:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.execute(f"USE `{DB_NAME}`")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trains (
                train_id INT PRIMARY KEY AUTO_INCREMENT,
                train_name VARCHAR(100) NOT NULL,
                source VARCHAR(100) NOT NULL,
                destination VARCHAR(100) NOT NULL,
                departure_time VARCHAR(30) NOT NULL,
                arrival_time VARCHAR(30) NOT NULL,
                available_seats INT NOT NULL DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT PRIMARY KEY AUTO_INCREMENT,
                passenger_name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(20) NOT NULL,
                train_id INT NOT NULL,
                travel_date DATE NOT NULL,
                seats INT NOT NULL,
                FOREIGN KEY (train_id) REFERENCES trains(train_id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
        """)

        # Add the sample trains only when the table is empty.
        cursor.execute("SELECT COUNT(*) FROM trains")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_trains = [
                ("Mangalore Express", "Kasaragod", "Mangalore", "06:30 AM", "09:00 AM", 100),
                ("Malabar Express", "Kasaragod", "Kozhikode", "08:00 AM", "11:30 AM", 120),
                ("Kannur Express", "Kasaragod", "Kannur", "10:15 AM", "12:00 PM", 80),
                ("Kerala Express", "Kasaragod", "Ernakulam", "02:00 PM", "08:00 PM", 150),
            ]
            cursor.executemany("""
                INSERT INTO trains
                (train_name, source, destination, departure_time, arrival_time, available_seats)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, sample_trains)

        connection.commit()
        return True

    except Error as error:
        connection.rollback()
        print("Database setup failed:", error)
        return False
    finally:
        cursor.close()
        connection.close()


def connect_db():
    """Connect directly to the ticket_booking database."""
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Error as error:
        print("Database connection failed:", error)
        return None


if __name__ == "__main__":
    if setup_database():
        connection = connect_db()
        if connection:
            print("Database connected successfully!")
            connection.close()
