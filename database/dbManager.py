import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#classe per la connessione ad DB
class DatabeseManager:
    def __init__(self):
        self.connection=None

#metodo per instaurare la connessione
def connection(self):
    try:
        self.connection=mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        print("Connessione al DB riuscita")

    except Exception as error:
        print(f"Connessione al DB non disponibile {error}")

#avvio la connessione
    def getconnection(self):
        return self.connection()
    
    #chiusura delle connessione
    def closeconnection(self):
        if self.connection():
            self.connection.close()
        print("Connessione al DB chiusa")

