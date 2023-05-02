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
            print(f"Image '{image}' loaded")
            face_image = face_recognition.load_image_file(image)

            face_encoding = face_recognition.face_encodings(face_image)[0]
            name, surname = filename[:filename.rfind(".")].split("_")
            self.db.save_employee(name=name, surname=surname, face_encoding=face_encoding)


if __name__ == '__main__':
    db = FacesDatabase()
    loader = ImageLoader(db)
    loader.load_employees_from_folder("/Users/ilakonovalov/PycharmProjects/turnstile-client/data")
