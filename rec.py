from Database import Database
from datetime import datetime

class Patient:
    
       
    def __init__(self):
        self.name=input("Enter Patient name: ")
        self.age=int(input("enter patient Age: "))
        self.Gender=input("Select gender : 'Male', 'Female', 'Other'")
        self.contact_info=input("Enter contact info : ")
        self.medical_history=None
    
    def add_patient(self):
        conn=Database.connect_db()
        if conn is None:
            return False
        

        cursor=conn.cursor()

        query= """
        INSERT INTO Patients (name, age, gender, contact_info)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (self.name, self.age, self.Gender, self.contact_info,))
        conn.commit()
        print("Patient added: ")
        cursor=conn.cursor()
        query2= "Select * from Patients where name=%s "
        cursor.execute(query2,(self.name,))
        result=cursor.fetchall()
        if result :
            for user in result:
                print(f"Patient ID: {user[0]} .   Patient Name: {user[1]}, Patient Age: {user[2]}, gender: {user[3]}" )
        conn.close()
        cursor.close()
        return result

    
    def View_patient():
        conn = Database.connect_db()
        if conn is None:
            print("Database connection failed.")
            return False

        cursor = conn.cursor()

        # Get the role of the logged-in user
        role_query = "SELECT role FROM users WHERE username = %s"
        user_name = input("Enter your username: ")  
        cursor.execute(role_query, (user_name,))
        user_role = cursor.fetchone()

        if not user_role:
            print("User not found or role not assigned.")
            return False

        role = user_role[0]  

        if role == "Receptionist":

            name=input("Enter patient_name: ")
            
            query = "SELECT name, age, contact_info FROM Patients where name= %s"
            cursor.execute(query,(name,))
            results = cursor.fetchall()
            if results:
                print("Patient Details (For Receptionist):")
                for patient in results:
                    print(f"Name: {patient[0]}, Age: {patient[1]}, Contact: {patient[2]}")
            else:
                print("No patients found.")
        elif role == "Doctor":
            name = input("Enter patient name: ")
            query = "SELECT name, age, gender, contact_info, medical_history, address FROM Patients WHERE name = %s"
            cursor.execute(query, (name,))
            results = cursor.fetchall()

            if results:
                print("Patient Details (For Doctor):")
                for patient in results:
                    
                    print(f"Name: {patient[0]}, Age: {patient[1]}, Gender: {patient[2]}, Contact: {patient[3]}, "
                          f"Medical History: {patient[4]}, Address: {patient[5]}")
            else:
                print("No patients found.")
        else:
            print("You are not authorized to view patient details.")

        
        cursor.close()
        conn.close()

        return True




    def delete_patient(name ):
        
        conn=Database.connect_db()
        cursor=conn.cursor()
        query = "DELETE FROM Patients WHERE name = %s"
        cursor.execute(query, (name,))
        conn.commit()
        print("Patient deleted successfully!")
    


    def update_patient(self,patient_id,):
        self.name==None,self.age==None, self.Gender==None, self.contact_info==None, self.medical_history==None
        
        
        updates = []
        params = []
        conn=Database.connect_db()

        cursor=conn.cursor()
        if self.name:
            updates.append("name = %s")
            params.append(self.name)
        if self.age:
            updates.append("age = %s")
            params.append(self.age)
        if self.Gender:
            updates.append("gender = %s")
            params.append(self.Gender)
        if self.contact_info:
            updates.append("contact_info = %s")
            params.append(self.contact_info)
        if self.medical_history:
            updates.append("medical_history = %s")
            params.append(self.medical_history)

        params.append(patient_id)
        query = f"UPDATE Patients SET {', '.join(updates)} WHERE patient_id = %s"
        cursor.execute(query, params)
        conn.commit()
        print("Patient updated successfully!")

 




    def assign_patient(name, doctor_name):
        conn = Database.connect_db()
        cursor = conn.cursor()

        # Fetch patient_id
        query0 = "SELECT patient_id FROM Patients WHERE name = %s"
        cursor.execute(query0, (name,))
        patient_result = cursor.fetchone()  

        if patient_result:
            patient_id = patient_result[0]  
        else:
            print(f"Patient {name} not found.")
            return

        # Fetch doctor_id
        query1 = "SELECT doctor_id FROM Doctors WHERE name = %s"
        cursor.execute(query1, (doctor_name,))
        doctor_result = cursor.fetchone()  

        if doctor_result:
            doctor_id = doctor_result[0]  # Extract the doctor_id from the tuple
        else:
            print(f"Doctor {doctor_name} not found.")
            return
        input_date = input("Enter appointment date (YYYY-MM-DD): ")
        try:
            appointment_date = datetime.strptime(input_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return

        time_input = input("Enter appointment time (HH:MM:SS): ")
        try:
            appointment_time = datetime.strptime(time_input, "%H:%M:%S").time()
        except ValueError:
            print("Invalid time format. Please enter in HH:MM:SS format.")
            return

        # Insert the appointment into the database
        query = """
            INSERT INTO Appointments (patient_id, doctor_id, date, time, status)
            VALUES (%s, %s, %s, %s, 'Scheduled')
        """
        cursor.execute(query, (patient_id, doctor_id, appointment_date, appointment_time))
        conn.commit()

        print(f"Patient {name} has been assigned to Doctor {doctor_name} on {appointment_date} at {appointment_time}.")

        conn.close()  
        cursor.close()
    
    def get_patient_name(self):
        return self.name


    @staticmethod
    def view_doctors():
        """Method to view all available doctors."""
        conn = Database.connect_db()
        if conn is None:
            print("Database connection failed.")
            return []

        cursor = conn.cursor()
        try:
            query = "SELECT doctor_id, name, specialization FROM Doctors"
            cursor.execute(query)
            doctors = cursor.fetchall()

            if doctors:
                print("Available Doctors:")
                for doc in doctors:
                    print(f"ID: {doc[0]}, Name: {doc[1]}, Specialization: {doc[2]}")
            else:
                print("No doctors found.")
            return doctors
        finally:
            cursor.close()
            conn.close()

class Main_For_Rec:
    def main_menu_rec():
        while True:
            print("Receptionist Menu:")
            print("1: Admit Patient in hospital")
            print("2: Discharge Patient")
            print("3: Update Patient info")
            print("4: Get Doctor Appointment for Patient")
            print("5: View Admitted Patients")
            print("6: Exit")
    
            choice = input("Select an option: ")
    
            if choice == "1":
                patient = Patient()
                patient.add_patient()
            elif choice == "2":
                patient = Patient
                delete=input("Enter Patient Name to discharge: ")
                patient.delete_patient(delete)
            elif choice == "3":
                patient_id = int(input("Enter Patient ID to update: "))
                patient = Patient()
                patient.update_patient(patient_id)
            elif choice == "4":
                
                doctors = Patient.view_doctors()
    
                if not doctors:
                    print("No doctors available to schedule appointments.")
                    continue
                
                
                p=input("Enter patient Name: ")
                doctor_name = input("Enter the doctor's name from the list above: ")
                Patient.assign_patient(p, doctor_name)
    
            elif choice == "5":
                patient = Patient
                patient.View_patient()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
    
    
    
    




