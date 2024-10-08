import datetime
import hashlib

from main_files.database.db_setting import Database, execute_query
from main_files.decorator.decorator_func import log_decorator

SUPERADMIN_LOGIN = "superadmin"
SUPERADMIN_PASSWORD = "password"


class Auth:
    def __init__(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__()
        self.__database = Database()

    @log_decorator
    def login(self):

        """
                Authenticate a user by checking their email and password.
                Updates the user's login status to True upon successful login.
        """

        email: str = input("Email: ").strip()
        password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()

        if email == SUPERADMIN_LOGIN and password == hashlib.sha256(SUPERADMIN_PASSWORD.encode('utf-8')).hexdigest():
            return {'is_login': True, 'role': 'super_admin'}

        query = '''
        SELECT * FROM users WHERE email=%s AND password=%s
        '''
        params = (email, password)
        user = execute_query(query, params, fetch='one')
        if user is None:
            query = '''
                    SELECT * FROM manager WHERE email=%s AND password=%s
            '''
            params = (email, password)
            manager = execute_query(query, params, fetch='one')
            if manager is None:
                print("Login failed")
                return False
            else:
                update_query = 'UPDATE manager SET status=True WHERE email=%s'
                execute_query(update_query, params=(email,))
                return {'is_login': True, 'role': 'manager'}
        else:
            update_query = 'UPDATE users SET status=TRUE WHERE email=%s'
            execute_query(update_query, params=(email,))
            return {'is_login': True, 'role': 'user'}

    @log_decorator
    def create_user_table(self):
        """
               Create the users table in the database if it does not already exist.
        """
        query = '''
                    CREATE TABLE IF NOT EXISTS users (
                    ID SERIAL PRIMARY KEY,
                    first_name VARCHAR(64) NOT NULL,
                    last_name VARCHAR(64) NOT NULL,
                    phone_number VARCHAR(64) NOT NULL,
                    role VARCHAR(64) NOT NULL DEFAULT 'customer',
                    email VARCHAR(64) NOT NULL,
                    password VARCHAR(255) UNIQUE NOT NULL,
                    status boolean DEFAULT FALSE NOT NULL,
                    created_at TIMESTAMP DEFAULT DATE_TRUNC('minute', NOW())
                    );
                '''
        with self.__database as cursor:
            cursor.execute(query)
        return True

    #
    # @log_decorator
    # def register(self):
    #     """
    #             Register a new user by adding their details to the users table.
    #     """
    #     # self.create_user_table()
    #     first_name: str = input("First Name: ")
    #     last_name: str = input("Last Name: ")
    #     email: str = input("Email: ")
    #     password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()
    #     confirm_password: str = hashlib.sha256(input("Confirm password: ").strip().encode('utf-8')).hexdigest()
    #     while password != confirm_password:
    #         print("Passwords do not match")
    #         password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()
    #         confirm_password: str = hashlib.md5(input("Confirm password: ").strip().encode('utf-8')).hexdigest()
    #     query = '''
    #                INSERT INTO "users" (FIRSTNAME, LASTNAME, EMAIL, PASSWORD)
    #                VALUES (%s, %s, %s, %s);
    #                '''
    #     params = (first_name, last_name, email, password)
    #     with self.__database as db:
    #         db.execute(query, params)
    #     print("User registered successfully")
    #     return None

    @log_decorator
    def logout(self):
        """
                Set the login status of all users to False (i.e., log out all users).
        """
        self.create_user_table()
        query = 'UPDATE users SET status=FALSE;'
        with self.__database as db:
            db.execute(query)
            return True
