import os
from datetime import datetime
import psycopg2
from flask import jsonify, make_response
from instance.config import Config


class Dtb():
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def connection(self):
        try:
            if os.getenv("APP_SETTINGS") == "testing":
                self.conn = psycopg2.connect(database="test_dtb",
                                             password=self.db_password,
                                             user=self.db_user,
                                             host=self.db_host
                                             )
            if os.getenv("APP_SETTINGS") == "development":
                self.conn = psycopg2.connect(
                    database=self.db_name,
                    password=self.db_password,
                    user=self.db_user,
                    host=self.db_host
                )

        except Exception as e:
            print(e)
        return self.conn

    def create_tables(self):
        tables = [

            """
            CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,
            username varchar(30) not null,
            email varchar(50) not null,
            password varchar(250) not null,
            role varchar(10) not null)
            """,
            """
                CREATE TABLE IF NOT EXISTS products (product_id serial PRIMARY KEY,
                title varchar(30) not null,
                description varchar(100) not null,
                price float(4) not null,
                quantity float(4) not null,
                lower_inventory int not null)
            """,

            """
                CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
                user_id int REFERENCES users(user_id) not null,
                product_id int REFERENCES products(product_id) not null)
            """
        ]
        try:
            cur = self.connection().cursor()
            for table in tables:
                cur.execute(table)
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cur = self.connection().cursor()

        sql = [
            "DROP TABLE IF EXISTS users CASCADE",
            "DROP TABLE IF EXISTS products CASCADE",
            "DROP TABLE IF EXISTS sales CASCADE"
        ]
        for query in sql:
            cur.execute(query)
        self.conn.commit()
        self.conn.close()

    def get_all_users(self):
        cur = self.connection().cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        users = []
        single_user = {}
        
        for user in result:
            single_user['user_id'] = user[0]
            single_user["username"] = user[1]
            single_user["email"] = user[2]
            single_user["password"] = user[3]
            single_user['role'] = user[4]
            users.append(single_user)

        self.conn.close()
        return users


class SaveUser(Dtb):
    def __init__(self, data):
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.role = data['role']

        db = Dtb()
        self.conn = db.connection()
        db.create_tables()
        # user_list = self.get_all_users()
        # save = True
        # for user in user_list:
        #     if user["username"] == username or user["email"] == email:
        #          save = False
        # save information to db

    def save_user(self):
        cursor = self.conn.cursor()
        # if save:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (self.username, self.email, self.password, self.role)
        )
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    db = Dtb()
    db.destroy_tables()
#     data = {"username": "sdkhkdh", "password": "kdjhhg",  "email": "dbjhdb", "role": "khajch"}
#     user = User(data)
#     user.save_user()
