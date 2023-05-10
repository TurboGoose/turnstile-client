import os
import time

import face_recognition

from benchmark.storage import Database
from core import processing, client


def load_employees(database, employees):
    for name, surname, image in employees:
        face_image = face_recognition.load_image_file(image)
        print(f"Employee '{name} {surname}' with image '{image}' loaded")
        face_encoding = face_recognition.face_encodings(face_image)[0]
        database.save_employee(name=name, surname=surname, face_encoding=face_encoding)


def setup_database(employees_data, database):
    database.drop_attendance_table()
    database.drop_employees_table()
    database.create_employees_table()
    database.create_attendance_table()
    load_employees(database, employees_data)
    client.reload_request()


def make_requests(employees_data):
    times = []
    for name, surname, image_path in employees_data:
        frame = face_recognition.load_image_file(image_path)
        start = time.time()
        processing.recognize_employee(frame)
        times.append(time.time() - start)
    return times


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
    num_runs = 10

    reference_employees = read_employees(reference)
    db = Database()
    setup_database(reference_employees, db)
    print("Database set up")
    db.close()

    employees_to_recognize = read_employees(to_recognize)
    avg_times_per_run = []
    for i in range(num_runs):
        time_per_request = make_requests(employees_to_recognize)
        avg_times_per_run.append(sum(time_per_request) / len(time_per_request))

    for i in range(len(avg_times_per_run)):
        print(f"Average time per request in run {i + 1}:", avg_times_per_run[i])
    print("Total average time for all runs:", sum(avg_times_per_run) / num_runs)
