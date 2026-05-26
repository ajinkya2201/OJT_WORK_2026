from database.db_connection import get_db_connection


connection = get_db_connection()

print("Database Connected Successfully")

connection.close()