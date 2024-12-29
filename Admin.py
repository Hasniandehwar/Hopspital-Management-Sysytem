from Database import Database


class Admin:

    @staticmethod
    def add_doctor():
        """Add a new doctor."""
        conn = Database.connect_db()
        cursor = conn.cursor()
        doctor_name = input("Enter Doctor's Name: ")
        specialization = input("Enter Doctor's Specialization: ")
        contact = input("Enter Doctor's Contact: ")
        schedule = input("Enter Doctor's Duty Time (in JSON format, e.g., {'Monday': '9AM-5PM'}): ")
        add_query = """
            INSERT INTO Doctors (name, specialization, contact_info, schedule) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(add_query, (doctor_name, specialization, contact, schedule))
            conn.commit()
            print("Doctor added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def update_doctor():
        """Update an existing doctor."""
        conn = Database.connect_db()
        cursor = conn.cursor()
        doctor_id = input("Enter Doctor's ID to update: ")
        updated_name = input("Enter Updated Name (leave blank to skip): ")
        updated_specialization = input("Enter Updated Specialization (leave blank to skip): ")
        updated_contact = input("Enter Updated Contact (leave blank to skip): ")
        updated_schedule = input("Enter Updated Duty Time (in JSON format, leave blank to skip): ")

        update_query = "UPDATE Doctors SET "
        update_values = []

        if updated_name:
            update_query += "name = %s, "
            update_values.append(updated_name)
        if updated_specialization:
            update_query += "specialization = %s, "
            update_values.append(updated_specialization)
        if updated_contact:
            update_query += "contact_info = %s, "
            update_values.append(updated_contact)
        if updated_schedule:
            update_query += "schedule = %s, "
            update_values.append(updated_schedule)

        # Remove trailing comma and add WHERE clause
        update_query = update_query.rstrip(", ") + " WHERE doctor_id = %s"
        update_values.append(doctor_id)

        try:
            cursor.execute(update_query, tuple(update_values))
            conn.commit()
            print("Doctor updated successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def delete_doctor():
        """Delete an existing doctor."""
        conn = Database.connect_db()
        cursor = conn.cursor()
        doctor_id = input("Enter Doctor's ID to delete: ")

        try:
            delete_query = "DELETE FROM Doctors WHERE doctor_id = %s"
            cursor.execute(delete_query, (doctor_id,))
            conn.commit()
            print(f"Doctor with ID {doctor_id} deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    @staticmethod
    def main_menu():
        while True:
            print("\n________________________Admin Panel________________________")
            print("1: Add Doctor")
            print("2: Update Doctor")
            print("3: Delete Doctor")
            print("4: Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                Admin.add_doctor()
            elif choice == "2":
                Admin.update_doctor()
            elif choice == "3":
                Admin.delete_doctor()
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")


