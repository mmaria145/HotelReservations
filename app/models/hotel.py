import re
from app.database.connection import get_connection


class Hotel:
    def __init__(self, hotel_id=None, name=None, address=None, phone_number=None):
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.phone_number = phone_number

    def create(self):
        if not self.valida():
            print("Datos inválidos. No se puede crear el hotel.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO hotels (name, address, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.name, self.address, self.phone_number))
        connection.commit()
        self.hotel_id = cursor.lastrowid
        cursor.close()
        connection.close()

    @staticmethod
    def read(hotel_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM hotels WHERE hotel_id = %s"
        cursor.execute(query, (hotel_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return Hotel(*result)
        return None

    @staticmethod
    def read_all():
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM hotels"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Hotel(*row) for row in results]

    def update(self):
        if not self.valida():
            print("Datos inválidos. No se puede actualizar el hotel.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE hotels SET name = %s, address = %s, phone_number = %s WHERE hotel_id = %s"
        cursor.execute(query, (self.name, self.address, self.phone_number, self.hotel_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM hotels WHERE hotel_id = %s"
        cursor.execute(query, (self.hotel_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def valida(self):
        if self.hotel_id is not None and not isinstance(self.hotel_id, int):
            print("ID del hotel debe ser un número.")
            return False
        if not self.name or not isinstance(self.name, str):
            print("Nombre del hotel inválido.")
            return False
        if not self.address or not isinstance(self.address, str):
            print("Dirección del hotel inválida.")
            return False
        if not re.match(r"^\d+$", self.phone_number):
            print("Número de teléfono inválido.")
            return False
        return True
