import re
from datetime import datetime
from app.database.connection import get_connection
from app.models.customer import Customer
from app.models.room import Room


class Reservation:
    def __init__(self, reservation_id=None, customer_id=None, room_id=None, check_in_date=None, check_out_date=None,
                 total_price=None, status=None):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_price = total_price
        self.status = status

    def create(self):
        if not self.valida():
            print("Datos inválidos. No se puede crear la reservación.")
            return
        self.calculate_total_price()
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO reservations (customer_id, room_id, check_in_date, check_out_date, total_price, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            self.customer_id, self.room_id, self.check_in_date, self.check_out_date, self.total_price, self.status))
        connection.commit()
        self.reservation_id = cursor.lastrowid
        cursor.close()
        connection.close()

    def calculate_total_price(self):
        room = Room.read(self.room_id)
        if room:
            check_in = datetime.strptime(self.check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(self.check_out_date, "%Y-%m-%d")
            nights = (check_out - check_in).days
            self.total_price = room.price_per_night * nights

    @staticmethod
    def read(reservation_id):
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM reservations WHERE reservation_id = %s"
        cursor.execute(query, (reservation_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return Reservation(*result)
        return None

    @staticmethod
    def read_all():
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM reservations"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Reservation(*row) for row in results]

    def update(self):
        if not self.valida():
            print("Datos inválidos. No se puede actualizar la reservación.")
            return
        self.calculate_total_price()
        connection = get_connection()
        cursor = connection.cursor()
        query = """
        UPDATE reservations SET customer_id = %s, room_id = %s, check_in_date = %s, check_out_date = %s, total_price = %s, status = %s
        WHERE reservation_id = %s
        """
        cursor.execute(query, (
            self.customer_id, self.room_id, self.check_in_date, self.check_out_date, self.total_price, self.status,
            self.reservation_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete(self):
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM reservations WHERE reservation_id = %s"
        cursor.execute(query, (self.reservation_id,))
        connection.commit()
        cursor.close()
        connection.close()

    def valida(self):
        if self.reservation_id is not None and not isinstance(self.reservation_id, int):
            print("ID de la reservación debe ser un número.")
            return False
        if not isinstance(self.customer_id, int):
            print("ID del cliente debe ser un número.")
            return False
        if not isinstance(self.room_id, int):
            print("ID de la habitación debe ser un número.")
            return False
        if not re.match(r"\d{4}-\d{2}-\d{2}", self.check_in_date):
            print("Fecha de check-in inválida. Debe ser en formato YYYY-MM-DD.")
            return False
        if not re.match(r"\d{4}-\d{2}-\d{2}", self.check_out_date):
            print("Fecha de check-out inválida. Debe ser en formato YYYY-MM-DD.")
            return False
        check_in = datetime.strptime(self.check_in_date, "%Y-%m-%d")
        check_out = datetime.strptime(self.check_out_date, "%Y-%m-%d")
        if check_in >= check_out:
            print("La fecha de check-in debe ser antes de la fecha de check-out y no pueden ser el mismo día.")
            return False
        if not self.customer_exists():
            print("El cliente con el ID proporcionado no existe.")
            return False
        if not self.room_exists():
            print("La habitación con el ID proporcionado no existe.")
            return False
        return True

    def customer_exists(self):
        customer = Customer.read(self.customer_id)
        return customer is not None

    def room_exists(self):
        room = Room.read(self.room_id)
        return room is not None

    def get_customer_name(self):
        customer = Customer.read(self.customer_id)
        if customer:
            return f"{customer.first_name} {customer.last_name}"
        return "Cliente no encontrado"

    def get_room_details(self):
        room = Room.read(self.room_id)
        if room:
            return f"Tipo: {room.room_type}, Precio por noche: {room.price_per_night}"
        return "Habitación no encontrada"
