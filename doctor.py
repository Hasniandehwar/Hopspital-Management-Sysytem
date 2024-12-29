from Database import Database
import csv
from datetime import datetime, date , timedelta
import os 
class doctors:
    def fetch_appointments(self,doctor_id):
        conn = Database.connect_db()
        cursor = conn.cursor()

        query = """
        SELECT a.date, a.time, p.name, p.contact_info
        FROM Appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = %s
        """
        cursor.execute(query, (doctor_id,))
        appointments = cursor.fetchall()

        conn.close()
        return appointments


    def view_appointments(self, doctor_id):
        appointments = self.fetch_appointments(doctor_id)

        if not appointments:
            print("\nNo appointments found.")
            return

        print("\nAppointments:")
        print(f"{'Date':<12} {'Time':<10} {'Patient Name':<20} {'Contact Info':<15}")
        print("-" * 60)

        for date_obj, time_obj, patient_name, contact_info in appointments:
            # Format the date if it's a datetime or date object
            if isinstance(date_obj, datetime):
                date_str = date_obj.strftime("%Y-%m-%d")
            elif isinstance(date_obj, date):  # For just date objects
                date_str = date_obj.strftime("%Y-%m-%d")

            # Format the time if it's a timedelta object
            if isinstance(time_obj, timedelta):
                hours = time_obj.seconds // 3600
                minutes = (time_obj.seconds // 60) % 60
                time_str = f"{hours:02}:{minutes:02}"
            else:
                time_str = str(time_obj)  # If it's already a string or other valid type

            print(f"{date_str:<12} {time_str:<10} {patient_name:<20} {contact_info:<15}")





    def generate_report(patient_id, doctor_id, diagnosis, prescription):
    
        # Connect to the database
        conn = Database.connect_db()
    
        cursor = conn.cursor()

        # Insert the report data into the Reports table
        query = """
            INSERT INTO Reports (patient_id, doctor_id, diagnosis, prescription)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (patient_id, doctor_id, diagnosis, prescription))
        
        # Commit the transaction
        conn.commit()

        print(f"Report successfully generated for patient {patient_id} by doctor {doctor_id}.")
        
    
        cursor.close()
        conn.close()

    def fetch_reports(doctor_id):
        conn=Database.connect_db()
        cursor = conn.cursor()

        # Fetch the reports for the specified doctor
        query = """
            SELECT r.report_id, p.name AS patient_name, d.name AS doctor_name, r.diagnosis, r.prescription, r.created_at
            FROM Reports r
            JOIN Patients p ON r.patient_id = p.patient_id
            JOIN Doctors d ON r.doctor_id = d.doctor_id
            WHERE r.doctor_id = %s;
        """
        cursor.execute(query, (doctor_id,))
        reports = cursor.fetchall()

        # Display the reports
        if reports:
            print("\nReports for Doctor:", doctor_id)
            print(f"{'Report ID':<10} {'Patient Name':<20} {'Diagnosis':<20} {'Prescription':<20} {'Created At'}")
            print("-" * 80)
            for report in reports:
                print(f"{report[0]:<10} {report[1]:<20} {report[3]:<20} {report[4]:<20} {report[5]}")
        else:
            print("\nNo reports found for this doctor.")

    
        cursor.close()
        conn.close()


    

class Doctor_Console: 
    def doctor_console(doctor_id):
        while True:
            print("\nDoctor Console")
            print("1. View Appointments")
            print("2. Generate Appointment Report")
            print("3. View Generated Reports")
            print("4. Exit")
            

            choice = input("Enter your choice: ")

            if choice == "1":
                doctors().view_appointments(doctor_id)
            elif choice == "2":
                diagnosis=input("Enter Patient Diagnose")
                prescription=input("Enter prescription From th patient ")
                Patient_id=input("patient_id: ")
                doctors.generate_report(Patient_id,doctor_id, diagnosis, prescription)
            elif choice == "3":
                doctors.fetch_reports(doctor_id)
            
            elif choice == "5":
                print("Exiting doctor console...")
                break
            else:
                print("Invalid choice. Please try again.")


