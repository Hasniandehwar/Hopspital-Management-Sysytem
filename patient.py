from Database import Database
from datetime import datetime
from rec import Patient
class Book_App:
    
    def View_doctors():
        conn=Database.connect_db()
        cursor=conn.cursor()

        query= "Select name,specialization from Doctors  "
        cursor.execute(query,)
        re=cursor.fetchall()

        if re:
            for i in re:
                print(f"DOCTOR : {i[0]} . Specialization {i[1]} .  ")
        return re
    
    def assign_patient(self, name, doctor_name):
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

        conn.close()  # Close the connection after the transaction
        cursor.close()





class Patient_menu(Book_App):
    

    @staticmethod
    def main_menu():
        while True:
            print("--------------------------------BOOk APPOINTMENT--------------------------")
            print("Choose from Options Give Below: ")
            print("1: view Doctors")
            print("2: Book an appointment: ")
    
            choice=input("Enter Your choice :")
    
            if choice=="1":
                patient=Book_App.View_doctors()
                return patient
            
            #Kareem 
    
            if choice=="2":
                # Step 1: Addd patient
                add_patient=Patient().add_patient()

                if not add_patient:
                    print("patient is not added: .")
                    continue
                # VIew Doctors 
                doctors = Book_App.View_doctors()
        
                if not doctors:
                    print("No doctors available to schedule appointments.")
                    continue

                    
                p=input("Enter patient Name: ")
        
                    # Step 4: Get doctor name from the user and assign the patient
                doctor_name = input("Enter the doctor's name from the list above: ")
                Book_App().assign_patient(p, doctor_name)
        

    