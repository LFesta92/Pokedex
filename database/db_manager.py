import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Gestisce una singola connessione MySQL riutilizzabile nell'app.
class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        # Se la connessione e gia aperta, la riutilizziamo.
        if self.connection and self.connection.is_connected():
            return self.connection

        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            return self.connection
        except mysql.connector.Error as error:
            print(f"Connessione MySQL non riuscita: {error}")
            self.connection = None
            return None

    def get_connection(self):
        # Punto di accesso unico usato dai service.
        return self.connect()

    def close_connection(self):
        # Chiude la connessione solo se e davvero attiva.
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
