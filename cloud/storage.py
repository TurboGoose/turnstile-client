import io
import os
import sqlite3

import face_recognition
import numpy as np

# DATABASE = "/Users/ilakonovalov/PycharmProjects/turnstile-client/data/data.db"
DATABASE = ":memory:"


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


sqlite3.register_adapter(np.ndarray, adapt_array)


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_converter("array", convert_array)


class FacesDatabase:

    def __init__(self, image_folder=None):
        self.connection = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        self.create_table()
        if image_folder is not None:
            self.load_employees_from_folder(image_folder)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def close(self):
        self.connection.close()

    def create_table(self):
        cur = self.connection.cursor()
        # TODO: add office attribute support
        cur.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL, 
            surname VARCHAR(50) NOT NULL,
            faceEncoding array NOT NULL);""")
        self.connection.commit()
        cur.close()

    def save_employee(self, employee_data):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO employees (name, surname, faceEncoding) values (?, ?, ?);", employee_data)
        generated_id = cur.lastrowid
        self.connection.commit()
        cur.close()
        return generated_id

    def get_all_faces(self):
        cur = self.connection.cursor()
        result_set = cur.execute("SELECT id, faceEncoding FROM employees;").fetchall()
        cur.close()

        ids = []
        encodings = []
        for id, encoding in result_set:
            ids.append(id)
            encodings.append(encoding)
        return ids, encodings

    def get_info_by_id(self, id):
        cur = self.connection.cursor()
        info = cur.execute("SELECT name, surname FROM employees WHERE id=?;", (id, )).fetchone()
        cur.close()
        return info

    def load_employees_from_folder(self, folder):
        try:
            for filename in os.listdir(folder):
                face_image = face_recognition.load_image_file(f"{folder}/{filename}")
                face_encoding = face_recognition.face_encodings(face_image)[0]
                name, surname = filename[:filename.rfind(".")].split("_")
                self.save_employee((name, surname, face_encoding))
        except FileNotFoundError:
            print(f"Image folder '{folder}' not exists")


if __name__ == '__main__':
    with FacesDatabase("../faces") as db:
        ids, encodings = db.get_all_faces()
        id = ids[0]
        encoding = encodings[0]
        creds = db.get_info_by_id(id)
        print(creds)
        print(id)
        print(encoding)


