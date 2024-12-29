import bcrypt
from Database import Database

class Auth:
    def Hash_a_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def check_user(self, user_name):
        conn = Database.connect_db()
        if conn is None:
            return False
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s"
        cursor.execute(query, (user_name,))  # Ensure tuple is passed
        r = cursor.fetchone()
        cursor.close()
        conn.close()
        return r is not None
    

    def registration(self, name , password, role):
        conn = Database.connect_db()
        if conn is None:
            print("Database connection failed.")
            return False
        hashed_password = self.Hash_a_password(password)
        cursor = conn.cursor()
        cursor.callproc('insert_user', (name, hashed_password, role))
        conn.commit()
        print("User registered successfully!")
        cursor.close()
        conn.close()
        return True

    def login(self, name , password):
        conn = Database.connect_db()
        if conn is None:
                return False
        
        try:
            cursor = conn.cursor()
            query = "SELECT password_hash FROM users WHERE username = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchone()

            if result:
                    stored_hash = result[0]
                    is_correct = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
                    if is_correct:
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password.")
                        return False
            else:
                    print("User not found.")
                    return False
        finally:
                cursor.close()
                conn.close()
