from database.db_connection import get_db_connection

def initialize_database():
    connection = get_db_connection()

    with open("database/schema.sql","r") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()

    print("Database tables created successfully")


initialize_database()