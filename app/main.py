from app.database.create_tables import create_tables
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.customer import Customer
from app.models.reservation import Reservation


def main_menu():
    print("Hola, bienvenido al programa para realizar reservas y consultas.")
    while True:
        print("\nMenú Principal:")
        print("a. Crear nuevo hotel")
        print("b. Crear nueva habitación")
        print("c. Crear nuevo cliente")
        print("d. Gestionar reservaciones")
        print("e. Salir")
        choice = input("Seleccione una opción: ")

        if choice == 'a':
            create_hotel()
        elif choice == 'b':
            create_room()
        elif choice == 'c':
            create_customer()
        elif choice == 'd':
            manage_reservations()
        elif choice == 'e':
            print("Gracias por usar el programa. ¡Adiós!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


def create_hotel():
    name = input("Ingrese el nombre del hotel: ")
    address = input("Ingrese la dirección del hotel: ")
    phone_number = input("Ingrese el número de teléfono del hotel: ")
    new_hotel = Hotel(name=name, address=address, phone_number=phone_number)
    new_hotel.create()
    print(f"Hotel '{new_hotel.name}' creado con éxito.")


def create_room():
    hotels = Hotel.read_all()
    if not hotels:
        print("No hay hoteles disponibles. Cree uno nuevo primero.")
        return

    print("\nHoteles disponibles:")
    for index, hotel in enumerate(hotels):
        print(f"{index + 1}. {hotel.name} - {hotel.address}")

    hotel_index = int(input("Seleccione el hotel por número: ")) - 1
    hotel_id = hotels[hotel_index].hotel_id

    room_number = input("Ingrese el número de la habitación: ")
    room_type = input("Ingrese el tipo de habitación: ")
    price_per_night = float(input("Ingrese el precio por noche: "))
    availability = input("¿Está disponible? (sí/no): ").lower() == 'sí'

    new_room = Room(hotel_id=hotel_id, room_number=room_number, room_type=room_type, price_per_night=price_per_night,
                    availability=availability)
    new_room.create()
    print(f"Habitación '{new_room.room_number}' creada con éxito.")


def create_customer():
    first_name = input("Ingrese el nombre del cliente: ")
    last_name = input("Ingrese el apellido del cliente: ")
    email = input("Ingrese el correo electrónico del cliente: ")
    phone_number = input("Ingrese el número de teléfono del cliente: ")
    new_customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    new_customer.create()
    print(f"Cliente '{new_customer.first_name} {new_customer.last_name}' creado con éxito.")


def manage_reservations():
    while True:
        print("\nSubmenú de Reservaciones:")
        print("1. Ver todas las reservaciones")
        print("2. Crear nueva reservación")
        print("3. Editar una reservación")
        print("4. Volver al menú principal")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            view_all_reservations()
        elif choice == '2':
            create_reservation()
        elif choice == '3':
            edit_reservation()
        elif choice == '4':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


def view_all_reservations():
    reservations = Reservation.read_all()
    if not reservations:
        print("No hay reservaciones disponibles.")
        return

    print("\nReservaciones existentes:")
    for reservation in reservations:
        print(
            f"ID: {reservation.reservation_id}, Cliente: {reservation.get_customer_name()}, Habitación: {reservation.get_room_details()}, Check-in: {reservation.check_in_date}, Check-out: {reservation.check_out_date}, Precio Total: {reservation.total_price}, Estado: {reservation.status}")


def create_reservation():
    customers = Customer.read_all()
    if not customers:
        print("No hay clientes disponibles. Cree uno nuevo primero.")
        return

    print("\nClientes disponibles:")
    for index, customer in enumerate(customers):
        print(f"{index + 1}. {customer.first_name} {customer.last_name}")

    customer_index = int(input("Seleccione el cliente por número: ")) - 1
    customer_id = customers[customer_index].customer_id

    rooms = Room.read_all()
    if not rooms:
        print("No hay habitaciones disponibles. Cree una nueva primero.")
        return

    print("\nHabitaciones disponibles:")
    for index, room in enumerate(rooms):
        print(f"{index + 1}. {room.room_number} - {room.room_type}")

    room_index = int(input("Seleccione la habitación por número: ")) - 1
    room_id = rooms[room_index].room_id

    check_in_date = input("Ingrese la fecha de check-in (YYYY-MM-DD): ")
    check_out_date = input("Ingrese la fecha de check-out (YYYY-MM-DD): ")
    status = input("Ingrese el estado de la reservación: ")

    new_reservation = Reservation(customer_id=customer_id, room_id=room_id, check_in_date=check_in_date,
                                  check_out_date=check_out_date, status=status)
    new_reservation.create()
    print(f"Reservación creada con éxito.")


def edit_reservation():
    reservations = Reservation.read_all()
    if not reservations:
        print("No hay reservaciones disponibles.")
        return

    print("\nReservaciones existentes:")
    for index, reservation in enumerate(reservations):
        print(
            f"{index + 1}. ID: {reservation.reservation_id}, Cliente: {reservation.get_customer_name()}, Habitación : {reservation.get_room_details()}")

    reservation_index = int(input("Seleccione la reservación por número: ")) - 1
    reservation = reservations[reservation_index]

    print(f"Editando reservación ID: {reservation.reservation_id}")
    customers = Customer.read_all()
    for index, customer in enumerate(customers):
        print(f"{index + 1}. {customer.first_name} {customer.last_name}")

    customer_index = int(input(f"Seleccione el nuevo cliente por número (actual: {reservation.customer_id}): ")) - 1
    reservation.customer_id = customers[customer_index].customer_id

    rooms = Room.read_all()
    for index, room in enumerate(rooms):
        print(f"{index + 1}. {room.room_number} - {room.room_type}")

    room_index = int(input(f"Seleccione la nueva habitación por número (actual: {reservation.room_id}): ")) - 1
    reservation.room_id = rooms[room_index].room_id

    reservation.check_in_date = input(f"Ingrese la nueva fecha de check-in (actual: {reservation.check_in_date}): ")
    reservation.check_out_date = input(f"Ingrese la nueva fecha de check-out (actual: {reservation.check_out_date}): ")
    reservation.status = input(f"Ingrese el nuevo estado de la reservación (actual: {reservation.status}): ")

    reservation.update()
    print(f"Reservación ID: {reservation.reservation_id} actualizada con éxito.")


if __name__ == '__main__':
    create_tables()
    print("Migración de la base de datos completada.")
    main_menu()
