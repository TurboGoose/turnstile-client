import os
import face_recognition

from storage import FacesDatabase


class ImageLoader:
    def __init__(self, face_db):
        self.db = face_db

    def load_employees_from_folder(self, folder):
        if not os.path.isdir(folder):
            print(f"Image folder '{folder}' does not exist")

        for filename in os.listdir(folder):
            image = f"{folder}/{filename}"
            face_image = face_recognition.load_image_file(image)
            print(f"Image '{image}' loaded")

            face_encoding = face_recognition.face_encodings(face_image)[0]
            name, surname = filename[:filename.rfind(".")].split("_")
            self.db.save_employee(name=name, surname=surname, face_encoding=face_encoding)

    def load_employees(self, employees):
        for name, surname, image in employees:
            face_image = face_recognition.load_image_file(image)
            print(f"Employee '{name} {surname}' with image '{image}' loaded")
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.db.save_employee(name=name, surname=surname, face_encoding=face_encoding)


DATASET_PATH = "/Users/ilakonovalov/PycharmProjects/turnstile-client/data/faces_dataset"


def read_employees():
    employees = []
    for file in os.listdir(DATASET_PATH):
        print("File: " + file)
        filename, extension = file.split(".")
        if extension != "normal":
            continue
        image = f"{DATASET_PATH}/{file}"
        name = filename.rstrip('0123456789')
        surname = filename[len(name):]
        employees.append((name, surname, image))
    return employees
