# app/main.py
from app.database.create_tables import create_tables

if __name__ == '__main__':
    create_tables()
    print("Migración de la base de datos completada.")