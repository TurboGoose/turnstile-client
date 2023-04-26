import io
import os
import sqlite3

import face_recognition
import numpy as np

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


def init_db(image_folder=None):
    create_table()
    if image_folder is not None:
        encode_faces(image_folder)


def create_table():
    con = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS faces (id INT PRIMARY KEY, name VARCHAR(50) NOT NULL,"
                " surname VARCHAR(50) NOT NULL, faceEncoding array NOT NULL);")
    cur.close()
    con.close()


def encode_faces(folder):
    try:
        data = []
        for filename in os.listdir(folder):
            face_image = face_recognition.load_image_file(f"{folder}/{filename}")
            face_encoding = face_recognition.face_encodings(face_image)[0]
            name, surname = filename[:filename.rfind(".")].split("_")
            data.append((name, surname, face_encoding))
        load_faces_from_images(data)
    except FileNotFoundError:
        print(f"Image folder '{folder}' not exists")


def load_faces_from_images(data):
    con = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.executemany("INSERT INTO faces (name, surname, faceEncoding) values (?, ?, ?)", *data)
    con.commit()
    cur.close()
    con.close()


def get_all_faces():
    con = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    faces = cur.execute("SELECT id, faceEncoding FROM faces").fetchall()
    cur.close()
    con.close()
    return faces


def get_info_by_id(id):
    con = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    info = cur.execute("SELECT name, surname FROM faces WHERE id=?", id).fetchone()
    cur.close()
    con.close()
    return info


class BatchLoader:
    def __init__(self, page_size):
        self.page_size = page_size
        self.cur_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.total_rows > self.page_size * self.cur_page:
            raise StopIteration()
        offset = self.cur_page * self.page_size
        res = self.cur.execute(f"SELECT id, faceEncoding FROM faces LIMIT {self.page_size} OFFSET {offset};")
        self.cur_page += 1
        return res.fetchall()

    def __enter__(self):
        self.con = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()
        self.total_rows = self.cur.execute("SELECT count(*) FROM faces;").fetchone()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()
