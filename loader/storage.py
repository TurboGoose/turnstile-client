import os
import pickle

import psycopg2 as psy


class FacesDatabase:

    def __init__(self, table_name="employees_test"):
        self.table_name = table_name

        db_connect_kwargs = {
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'dbname': os.getenv('POSTGRES_DBNAME'),
            'host': os.getenv('POSTGRES_HOST'),
            'port': os.getenv('POSTGRES_PORT')
        }

        print(f"DB connection URL:"
              f"postgres://{db_connect_kwargs['user']}:{db_connect_kwargs['password']}"
              f"@{db_connect_kwargs['host']}:{db_connect_kwargs['port']}/{db_connect_kwargs['dbname']}")

        self.connection = psy.connect(**db_connect_kwargs)
        self.connection.set_session(autocommit=True)

        self.create_table()

    def close(self):
        self.connection.close()

    def create_table(self):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL, 
                surname VARCHAR(50) NOT NULL,
                face_encoding BYTEA NOT NULL);""")
            cur.close()
        except psy.DatabaseError as err:
            print(err)

    def save_employee(self, name, surname, face_encoding):
        sql = f"INSERT INTO {self.table_name} (name, surname, face_encoding) VALUES (%s, %s, %s) RETURNING id;"
        try:
            face_encoding = pickle.dumps(face_encoding)
            cur = self.connection.cursor()
            cur.execute(sql, (name, surname, face_encoding))
            generated_id = cur.fetchone()[0]
            cur.close()
            return generated_id
        except psy.DatabaseError as err:
            print(err)

    def truncate_table(self):
        sql = f"TRUNCATE TABLE {self.table_name};"
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            cur.close()
        except psy.DatabaseError as err:
            print(err)

    def count_rows(self):
        sql = f"SELECT count(*) FROM {self.table_name};"
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            count = cur.fetchone()[0]
            cur.close()
            return count
        except psy.DatabaseError as err:
            print(err)
