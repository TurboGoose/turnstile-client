import os
import time

import face_recognition

from benchmark.storage import FacesDatabase
from core import processing, client


def load_employees(database, employees):
    for name, surname, image in employees:
        face_image = face_recognition.load_image_file(image)
        print(f"Employee '{name} {surname}' with image '{image}' loaded")
        face_encoding = face_recognition.face_encodings(face_image)[0]
        database.save_employee(name=name, surname=surname, face_encoding=face_encoding)


def setup_database(employees_data, database):
    database.drop_table()
    database.create_table()
    load_employees(database, employees_data)
    client.reload_request()


def make_requests(employees_data):
    for name, surname, image_path in employees_data:
        frame = face_recognition.load_image_file(image_path)
        credentials = processing.recognize_employee(frame)
        if not credentials:
            print("Not recognized")
            continue
        assert credentials["name"] == name
        assert credentials["surname"] == surname
        print(f'Employee "{name} {surname}" recognized\n')


def read_employees(folder):
    employees = []
    for file in os.listdir(folder):
        filename, extension = file.split(".")
        image_path = f"{folder}/{file}"
        name, surname = filename.split("_")
        employees.append((name, surname, image_path))
    return employees


def run():
    reference = "benchmark/data/reference"
    to_recognize = "benchmark/data/to_recognize"

    db = FacesDatabase()

    reference_employees = read_employees(reference)
    setup_database(reference_employees, db)
    print("Database set up")

    employees_to_recognize = read_employees(to_recognize)
    start = time.time()
    make_requests(employees_to_recognize)
    print("Elapsed time:", time.time() - start)
    db.close()
