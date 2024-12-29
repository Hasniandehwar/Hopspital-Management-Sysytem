import mysql.connector



class Database:
    def connect_db():
        try:
            conn = mysql.connector.connect(
            host='',  
            user='',  
            password='',  
            database=''  
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return None



