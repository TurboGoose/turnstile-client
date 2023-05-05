import os
import pickle

import psycopg2 as psy


class Database:
    def __init__(self):
        self.connection = None
        self.open()
        self.create_faces_table()
        self.create_attendance_table()

    def open(self):
        db_connect_kwargs = {
            'dbname': os.getenv('POSTGRES_DBNAME'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'host': os.getenv('POSTGRES_HOST'),
            'port': os.getenv('POSTGRES_PORT')
        }

        print(f"DB connection URL:"
              f"postgres://{db_connect_kwargs['user']}:{db_connect_kwargs['password']}"
              f"@{db_connect_kwargs['host']}:{db_connect_kwargs['port']}/{db_connect_kwargs['dbname']}")
        self.connection = psy.connect(**db_connect_kwargs)
        self.connection.set_session(autocommit=True)

    def close(self):
        self.connection.close()
        self.connection = None

    def reload(self):
        self.close()
        self.open()

    def create_faces_table(self):
        try:
            cur = self.connection.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL, 
                surname VARCHAR(50) NOT NULL,
                face_encoding BYTEA NOT NULL);""")
            cur.close()
        except psy.DatabaseError as err:
            print(err)

    def save_employee(self, name, surname, face_encoding):
        sql = f"INSERT INTO employees (name, surname, face_encoding) VALUES (%s, %s, %s) RETURNING id;"
        try:
            face_encoding = pickle.dumps(face_encoding)
            cur = self.connection.cursor()
            cur.execute(sql, (name, surname, face_encoding))
            generated_id = cur.fetchone()[0]
            cur.close()
            return generated_id
        except psy.DatabaseError as err:
            print(err)

    def get_all_faces(self):
        try:
            cur = self.connection.cursor()
            cur.execute("SELECT id, face_encoding FROM employees;")
            result_set = cur.fetchall()
            cur.close()

            ids = []
            encodings = []
            for id, encoding in result_set:
                ids.append(id)
                encodings.append(pickle.loads(encoding))
            return ids, encodings
        except psy.DatabaseError as err:
            print(err)

    def get_employee_credentials_by_id(self, id):
        sql = "SELECT id, name, surname FROM employees WHERE id = %s;"
        try:
            cur = self.connection.cursor()
            cur.execute(sql, (id,))
            info = cur.fetchone()
            cur.close()
            return info
        except psy.DatabaseError as err:
            print(err)

    def create_attendance_table(self):
        sql = """CREATE TABLE IF NOT EXISTS attendance (
                id SERIAL PRIMARY KEY,
                employee_id INT REFERENCES employees(id), 
                authorized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            cur.close()
        except psy.DatabaseError as err:
            print(err)

    def save_attendance_entry(self, employee_id):
        sql = f"INSERT INTO attendance (employee_id) VALUES (%s);"
        try:
            cur = self.connection.cursor()
            cur.execute(sql, (employee_id,))
            cur.close()
        except psy.DatabaseError as err:
            print(err)
