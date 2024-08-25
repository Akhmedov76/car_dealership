import datetime
import hashlib

from main_files.database.db_setting import Database, execute_query
from main_files.decorator.decorator_func import log_decorator
from main import super_admin_menu

SUPERADMIN_LOGIN ="superadmin"
SUPERADMIN_PASSWORD ="password"


class Auth:
    def __init__(self):
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").__str__()
        self.__database = Database()
        self.__super_admin = {'email': 'alamovasad@gmail.com', 'password': '000'}

    # @log_decorator
    # def login(self):
    #     threading.Thread(target=self.create_user_table).start()
    #     """
    #             Authenticate a user by checking their email and password.
    #             Updates the user's login status to True upon successful login.
    #     """
    #     email: str = input("Email: ").strip()
    #     password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()
    #     user = execute_query("SELECT * FROM users WHERE EMAIL=%s", (email,), fetch='one')

    #     if user is None:
    #         print("Login failed")
    #         return False
    #     elif user['password'] == password and user['email'] == email:
    #         query = '''UPDATE users SET IS_LOGIN=%s WHERE EMAIL=%s;'''
    #         params = (True, email)
    #         with self.__database as db:
    #             db.execute(query, params)
    #             print('Login successful')
    #             return True
    #     return False

    @log_decorator
    def login(self):

        # threading.Thread(target=self.create_user_table).start()


        """
                Authenticate a user by checking their email and password.
                Updates the user's login status to True upon successful login.
        """

        email: str = input("Email: ").strip()
        password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()

        if email ==SUPERADMIN_LOGIN and password ==SUPERADMIN_PASSWORD:
            return super_admin_menu()
        
        user = execute_query("SELECT * FROM customer WHERE EMAIL=%s" and "SELECT * FROM manager WHERE EMAIL=%s", (email,), fetch='one')


        if email == self.__super_admin['email']:
            if hashlib.sha256(password.encode()).hexdigest() == self.__super_admin['password']:
                return {'is_login': True, 'role': 'super_admin'}
        user = execute_query("SELECT * FROM users WHERE EMAIL=%s" and "SELECT * FROM manager WHERE EMAIL=%s", (email,),
                             fetch='one')


        if user is None:
            print("Login failed")
            return False
        elif user['password'] == password and user['email'] == email:
            query = '''UPDATE users SET IS_LOGIN=%s WHERE EMAIL=%s;'''
            params = (True, email)
            with self.__database as db:
                db.execute(query, params)
                print('Login successful')
                return True
        return False

    @log_decorator
    def create_user_table(self):
        """
               Create the users table in the database if it does not already exist.
        """
        query = '''
        CREATE TABLE IF NOT EXISTS USERS (
        ID SERIAL PRIMARY KEY,
        FIRSTNAME VARCHAR(255) NOT NULL,
        LASTNAME VARCHAR(255) NOT NULL,
        EMAIL VARCHAR(255) NOT NULL UNIQUE,
        PASSWORD VARCHAR(256) NOT NULL,
        IS_LOGIN BOOLEAN DEFAULT FALSE,
        CREATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
        with self.__database as cursor:
            cursor.execute(query)
        return True

    @log_decorator
    def register(self):
        """
                Register a new user by adding their details to the users table.
        """
        self.create_user_table()
        first_name: str = input("First Name: ")
        last_name: str = input("Last Name: ")
        email: str = input("Email: ")
        password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()
        confirm_password: str = hashlib.sha256(input("Confirm password: ").strip().encode('utf-8')).hexdigest()
        while password != confirm_password:
            print("Passwords do not match")
            password: str = hashlib.sha256(input("Password: ").strip().encode('utf-8')).hexdigest()
            confirm_password: str = hashlib.md5(input("Confirm password: ").strip().encode('utf-8')).hexdigest()
        query = '''
               INSERT INTO "users" (FIRSTNAME, LASTNAME, EMAIL, PASSWORD)
               VALUES (%s, %s, %s, %s);
               '''
        params = (first_name, last_name, email, password)
        with self.__database as db:
            db.execute(query, params)
        print("User registered successfully")
        return None

    @log_decorator
    def logout(self):
        """
                Set the login status of all users to False (i.e., log out all users).
        """
        self.create_user_table()
        query = 'UPDATE users SET IS_LOGIN=FALSE;'
        with self.__database as db:
            db.execute(query)
            return True
