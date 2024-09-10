import re
from app.database.connection import get_connection

class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None, phone_number=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    def create(self):
        if not self.valida():
            print("Datos inválidos. No se puede crear el cliente.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (self.first_name, self.last_name, self.email, self.phone_number))
        connection.commit()
        self.customer_id = cursor.lastrowid
        cursor.close()
        connection.close()

    @staticmethod
    def read(customer_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return Customer(*result)
        return None

    @staticmethod
    def read_all():
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM customers"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Customer(*row) for row in results]

    def update(self):
        if not self.valida():
            print("Datos inválidos. No se puede actualizar el cliente.")
            return
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE customers SET first_name = %s, last_name = %s, email = %s, phone_number = %s WHERE customer_id = %s"
        cursor.execute(query, (self.first_name, self.last_name, self.email, self.phone_number, self.customer_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM customers WHERE customer_id = %s"
        cursor.execute(query, (self.customer_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def valida(self):
        if self.customer_id is not None and not isinstance(self.customer_id, int):
            print("ID del cliente debe ser un número.")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            print("Correo electrónico inválido.")
            return False
        if not re.match(r"^\d+$", self.phone_number):
            print("Número de teléfono inválido.")
            return False
        if not self.first_name or not isinstance(self.first_name, str):
            print("Nombre del cliente inválido.")
            return False
        if not self.last_name or not isinstance(self.last_name, str):
            print("Apellido del cliente inválido.")
            return False
        return True