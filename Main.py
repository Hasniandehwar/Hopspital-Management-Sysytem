from login_signup import Auth
from Database import Database
from rec import Main_For_Rec
from doctor import Doctor_Console
from patient import Patient_menu
from Admin import Admin
def main_menu():
    while True:
        print("________________________Welcome to City Hospital______________________________")
        print("Choose an option:\n")
        print("1: Apply for registration")
        print("2: Login")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter Your Good Name: ")
            password = input("Enter your password: ")
            role = input("Enter your role (Admin, Doctor, Receptionist, Patient): ").capitalize()
            Auth().registration(name, password, role)

        elif choice == "2":
            conn = Database.connect_db()
            cursor = conn.cursor()

            name = input("Enter Your Good Name: ")
            password = input("Enter your password: ")

            # Fetch user role
            role_query = "SELECT role FROM users WHERE username = %s"
            cursor.execute(role_query, (name,))
            user_role = cursor.fetchone()

            if not user_role:
                print("User not found or role not assigned.")
                continue  # Return to the main menu

            role = user_role[0]

            # Authentication check
            if Auth().login(name, password):
                if role == "Receptionist":
                    Main_For_Rec.main_menu_rec()

                elif role == "Doctor":
                    query = "SELECT doctor_id FROM Doctors WHERE name = %s"
                    cursor.execute(query, (name,))
                    doctor_id = cursor.fetchone()

                    if doctor_id:
                        Doctor_Console.doctor_console(doctor_id[0])
                    else:
                
                        print("Doctor ID not found. Please contact the admin.")
                elif role=="Patient":
                      Patient_menu.main_menu()

                elif role=="Admin":
                    Admin.main_menu()
                        
                else:
                    print(f"Role '{role}' has no specific functionality implemented yet.")
            else:
                print("Login failed. Please check your credentials.")
        else:
            print("Invalid choice. Please try again.")



main_menu()