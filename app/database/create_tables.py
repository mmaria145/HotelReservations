# app/database/create_tables.py
from .connection import get_connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hotels (
        hotel_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INT AUTO_INCREMENT PRIMARY KEY,
        hotel_id INT,
        room_number VARCHAR(10) NOT NULL,
        room_type VARCHAR(50) NOT NULL,
        price_per_night DECIMAL(10, 2) NOT NULL,
        availability BOOLEAN NOT NULL,
        FOREIGN KEY (hotel_id) REFERENCES hotels (hotel_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        room_id INT,
        check_in_date DATE NOT NULL,
        check_out_date DATE NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        status VARCHAR(50) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
        FOREIGN KEY (room_id) REFERENCES rooms (room_id)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_tables()