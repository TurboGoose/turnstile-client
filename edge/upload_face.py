import os

import face_recognition

import core.client
from live.live_recognition import convert_frame


def upload_face(image_path, name=None, surname=None):
    if name is None and surname is None:
        file = os.path.normpath(image_path).split(os.sep)[-1]
        filename, extension = file.split(".")
        name, surname = filename.split("_")

    frame = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(convert_frame(frame))[0]
    core.client.save_request(name, surname, encoding)


if __name__ == '__main__':
    upload_face("../data/barak_obama.png")
