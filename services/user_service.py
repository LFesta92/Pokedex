from services.secutity_manager import SecurityManager

class UserService:

    def __init__(self,db_manager):
        self.db_manager=db_manager

    def register_user(self,username:str, password:str, email:str)->bool:
        connection=self.db_manager.get_connection()
        if not connection:
            print("Connessione al DB non disponibile")
            return False

        cursor=connection.cursor()

        try:
            check_query="SELECT id_utente FROM utenti WHERE username=%s OR email=%s"
            cursor.execute(check_query,(username,email))
            existing_user=cursor.fetchone()   

            if existing_user:
                print("Username già esistente")
                return False
            
            password_hash=SecurityManager.hash_password(password)
            insert_query="""INSERT INTO utenti (
            username, 
            password_hash, 
            email) VALUES ( 
            %s, 
            %s, 
            %s)"""
            cursor.execute(insert_query,(username,password_hash,email))
            connection.commit()
            print("Utente registrato con successo")
            return True
        
        except Exception as error:
            print(f"Errore nella registrazione utente {error}")
            connection.rollback()
            return False
        
        finally:
            cursor.close()

    
    
    
    def login(self, username:str, password:str):
        connection=self.db_manager.get_connection()
        if not connection:
            print("Connessione al DB non disponibile")
            return None      
        
        cursor=connection.cursor(dictionary=True)

        try:
            query="""SELECT * FROM utenti 
                    WHERE username=%s"""
             
            cursor.execute(query,(username,))
            user=cursor.fetchone()

            if not user:
                print("Utente non trovato")   
                return None
            
            if SecurityManager.verify_password(password,user['password_hash']):
                print("Login effettuato con successo")
                return user
            
            print("Password errata")
            return None

        except Exception as error:
            print(f"Errore durante il login {error}")
            connection.rollback()
            return None
        
        finally:
            cursor.close()

    def get_user_by_username(self, username: str):
        connection = self.db_manager.get_connection()
        if not connection:
            print("Connessione al DB non disponibile")
            return None

        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT id_utente, username, email FROM utenti WHERE username=%s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except Exception as error:
            print(f"Errore nel recupero utente {error}")
            return None
        finally:
            cursor.close()
