import hashlib
import threading

from email_sender.email import send_mail
from main_files.database.db_setting import Database, execute_query
from main_files.decorator.decorator_func import log_decorator


class Manager:
    def __init__(self):
        self.db = Database()

    @log_decorator
    def create_manager_table(self):
        """
        Create the manager table in the database if it does not already exist.
        """
        query = """
                CREATE TABLE IF NOT EXISTS manager (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone_number VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) UNIQUE NOT NULL,
                    status BOOLEAN DEFAULT False NOT NULL,
                    filial_id INTEGER REFERENCES filials(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        with self.db as cursor:
            cursor.execute(query)
            return None

    # def get_color_name_by_id(self, color_id):
    #     """
    #     Retrieve the color name based on the color_id.
    #     """
    #
    #     query = "SELECT name FROM color WHERE ID = %s"
    #     with self.db as cursor:
    #         cursor.execute(query, (color_id,))
    #         color_name = cursor.fetchone()
    #         if color_name:
    #             return color_name[0]
    #         else:
    #             return None

    @log_decorator
    def add_manager(self):
        """
        Add a new manager to the database.
        """
        threading.Thread(target=self.create_manager_table()).start()
        name = input("Manager Name: ").strip()

        while True:
            email = input("Manager Email: ").strip()
            if email.endswith("@gmail.com"):
                query_check = "SELECT * FROM manager WHERE email = %s"
                result = threading.Thread(execute_query(query_check, params=(email,), fetch="one")).start()
                if result:
                    print("Error! A manager with this email already exists.")
                else:
                    break
            else:
                print("Error! Email must end with '.gmail.com'!!!")

        phone_number = input("Manager Phone Number: ").strip()
        password = input("Manager Password: ").strip()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        subject = "You logged in: "
        message = f"Login: {email}\nPassword: {password}\n"

        filial_id = input("Filial ID: ").strip()

        query = """
        INSERT INTO manager (name, email, phone_number, password, filial_id) 
        VALUES (%s, %s, %s, %s, %s);
        """

        try:
            threading.Thread(target=send_mail, args=(email, subject, message)).start()
            threading.Thread(target=execute_query,
                             args=(query, (name, email, phone_number, hashed_password, filial_id))).start()

            print(f"Manager '{name}' added successfully.")
            return None
        except Exception as e:
            print(f"Failed to add manager: {e}")
            return None

    @log_decorator
    def update_manager(self):
        """
        Update the details of a manager in the database.
        """
        manager_id = int(input("Enter manager ID: "))
        name = input("Enter new manager name: ").strip()
        email = input("Enter new manager email: ").strip()
        phone_number = input("Enter new manager phone number: ").strip()
        filial_id = input("Enter new filial ID: ")
        query = """UPDATE manager SET name=%s, email=%s, phone_number=%s, filial_id=%s WHERE id=%s;"""
        try:
            execute_query(query, (name, email, phone_number, filial_id, manager_id))
            print(f"Manager details updated successfully.")
        except Exception as e:
            print(f"Failed to update manager: {e}")

    @log_decorator
    def delete_manager(self):
        """
        Delete a manager from the database.
        """
        manager_id = int(input("Enter manager ID: "))
        query = "DELETE FROM manager WHERE id=%s"
        try:
            execute_query(query, (manager_id,))
            print(f"Manager ID {manager_id} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete manager: {e}")

    @log_decorator
    def show_all_managers(self):
        """
        Show all managers in the manager table.
        """
        query = "SELECT * FROM manager;"
        result = execute_query(query, fetch="all")
        if result:
            print("Managers:")
            for manager in result:
                print(
                    f"ID: {manager[0]}, Name: {manager[1]}, Email: {manager[2]}, Phone Number: {manager[3]}, Filial ID: {manager[4]}")
        else:
            print("No managers found.")

    @log_decorator
    def search_manager(self):
        """
        Search for managers by name in the manager table.
        """
        name = input("Manager Name: ")
        query = "SELECT * FROM manager WHERE name LIKE %s;"
        result = execute_query(query, params=("%" + name + "%",), fetch="all")
        if result:
            print("Managers:")
            for manager in result:
                print(
                    f"ID: {manager[0]}, Name: {manager[1]}, Email: {manager[2]}, Phone Number: {manager[3]}, Filial ID: {manager[4]}")
        else:
            print("No managers found.")
