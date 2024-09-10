import re
from app.database.connection import get_connection
from app.models.hotel import Hotel


class Room:
    def __init__(self, room_id=None, hotel_id=None, room_number=None, room_type=None, price_per_night=None,
                 availability=None):
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.availability = availability

    def create(self):
        if not self.valida():
            print("Datos inválidos. No se puede crear la habitación.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO rooms (hotel_id, room_number, room_type, price_per_night, availability) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,
                       (self.hotel_id, self.room_number, self.room_type, self.price_per_night, self.availability))
        connection.commit()
        self.room_id = cursor.lastrowid
        cursor.close()
        connection.close()

    @staticmethod
    def read(room_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM rooms WHERE room_id = %s"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return Room(*result)
        return None

    @staticmethod
    def read_all():
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM rooms"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Room(*row) for row in results]

    def update(self):
        if not self.valida():
            print("Datos inválidos. No se puede actualizar la habitación.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE rooms SET hotel_id = %s, room_number = %s, room_type = %s, price_per_night = %s, availability = %s WHERE room_id = %s"
        cursor.execute(query, (
            self.hotel_id, self.room_number, self.room_type, self.price_per_night, self.availability, self.room_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM rooms WHERE room_id = %s"
        cursor.execute(query, (self.room_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def valida(self):
        if self.room_id is not None and not isinstance(self.room_id, int):
            print("ID de la habitación debe ser un número.")
            return False
        if not isinstance(self.hotel_id, int):
            print("ID del hotel debe ser un número.")
            return False
        if not self.room_number or not isinstance(self.room_number, str):
            print("Número de la habitación inválido.")
            return False
        if not self.room_type or not isinstance(self.room_type, str):
            print("Tipo de habitación inválido.")
            return False
        if not isinstance(self.price_per_night, (int, float)):
            print("El precio por noche debe ser un número.")
            return False
        if not isinstance(self.availability, bool):
            print("La disponibilidad debe ser un valor booleano.")
            return False
        if not self.hotel_exists():
            print("El hotel con el ID proporcionado no existe.")
            return False
        return True

    def hotel_exists(self):
        hotel = Hotel.read(self.hotel_id)
        return hotel is not None
