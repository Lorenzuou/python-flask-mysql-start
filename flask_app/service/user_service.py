import mysql.connector
from mysql.connector import Error




class UserService:
    def __init__(self, host='db', port=3306, user='root', password='password', database='mydatabase'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def create_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error: '{e}'")
            return None
        
    def check_user_credentials(self, username, password):
        connection = self.create_db_connection()
        print(connection)
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s",
                           (username, password,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user

    def insert_new_user(self, username, password, email):
        connection = self.create_db_connection()
        print(connection)
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO User (username, password, email) VALUES (%s, %s, %s)",
                           (username, password, email))
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return user_id
