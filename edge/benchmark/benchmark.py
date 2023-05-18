import os
import pickle
import time

import face_recognition

from Profiler import Profiler
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
    num_runs = 10
    output_filename = f"results{num_runs}.pickle"
    reference_folder = "benchmark/data/reference"
    to_recognize_folder = "benchmark/data/to_recognize"

    reference_employees = read_employees(reference_folder)
    db = Database()
    setup_database(reference_employees, db)
    db.close()

    employees_to_recognize = read_employees(to_recognize_folder)

    if os.path.exists(output_filename):
        os.remove(output_filename)

    with open(output_filename, "a+b") as outfile:
        for i in range(num_runs):
            profiler = Profiler()
            profiler.start()
            request_times = make_requests(employees_to_recognize)
            profiler.stop()
            cpu_usage, mem_usage = profiler.get_results()
            pickle.dump((request_times, cpu_usage, mem_usage), outfile)
