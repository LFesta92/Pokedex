class BoxServices:
    def __init__(self,db_manager):
        self.db_manager=db_manager


    #metodo per l'aggiunta di pokemon al box all'interno del DB
    def add_pokemon(self,id_utente:int,id_pokemon_api:int,nome_pokemon:str):
        connection=self.db_manager.get_connection()
        if not connection:
            print("Connessione al DB non disponibile")
            return False
        
        cursor=connection.cursor()

        try:
            check_query = "SELECT id_box FROM box WHERE id_utente=%s AND id_pokemon_api=%s"
            cursor.execute(check_query, (id_utente, id_pokemon_api))
            if cursor.fetchone():
                return False

            query = """
                INSERT INTO box (id_utente, id_pokemon_api, nome_pokemon)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_utente, id_pokemon_api, nome_pokemon))
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally:
            cursor.close()

    def has_pokemon(self, id_utente: int, id_pokemon_api: int):
        connection = self.db_manager.get_connection()
        if not connection:
            print("Connessione al DB non disponibile")
            return None

        cursor = connection.cursor()
        try:
            query = "SELECT id_box FROM box WHERE id_utente=%s AND id_pokemon_api=%s"
            cursor.execute(query, (id_utente, id_pokemon_api))
            return cursor.fetchone() is not None
        except Exception as error:
            print(f"Controllo box non riuscito {error}")
            return None
        finally:
            cursor.close()



    #metodo per recuperare i Pokèmon dal box
    def get_pokemon(self,id_utente:int):
        connection=self.db_manager.get_connection()
        
        if not connection:
            print("Connessione al DB non disponibile")
            return []
        
        cursor=connection.cursor(dictionary=True)

        try:
            query="SELECT id_pokemon_api, nome_pokemon FROM box WHERE id_utente=%s"
            cursor.execute(query,(id_utente,))
            return cursor.fetchall()

        except Exception as error:
            print(f"Recupero Pokèmon non possibile {error}")
            return []

        finally:
            cursor.close()    
