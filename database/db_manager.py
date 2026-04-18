import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

#classe per la connessione ad DB
class DatabaseManager:
    def __init__(self):
        self.connection=None

#metodo per instaurare la connessione
    def connect(self):
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
    
    #avvio la connessione
    def get_connection(self):
        return self.connect()
    
    #chiusura delle connessione
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

