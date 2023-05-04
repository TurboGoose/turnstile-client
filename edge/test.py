import os

import cv2
import face_recognition

import core.client


def convert_frame(frame):
    return cv2.cvtColor(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25), cv2.COLOR_BGR2RGB)


def test():
    ref = face_recognition.load_image_file("/Users/ilakonovalov/PycharmProjects/turnstile-client/edge/benchmark/data/reference/subject01.normal")
    rec = face_recognition.load_image_file("/Users/ilakonovalov/download.jpeg")

    ref_face_location = face_recognition.face_locations(ref)[0]
    rec_face_location = face_recognition.face_locations(rec)[0]

    ref_encoding = face_recognition.face_encodings(ref, [ref_face_location])[0]
    rec_encoding = face_recognition.face_encodings(rec, [rec_face_location])[0]
    print(ref_encoding)
    print(rec_encoding)

    print(face_recognition.face_distance(rec_encoding, [ref_encoding]))
    print(face_recognition.compare_faces(ref_encoding, [rec_encoding], tolerance=0.5))

    while True:
        if ref_face_location:
            top, right, bottom, left = ref_face_location
            cv2.rectangle(ref, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(ref, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        if rec_face_location:
            top, right, bottom, left = rec_face_location
            cv2.rectangle(rec, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(rec, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        cv2.imshow('Reference', ref)
        cv2.imshow('To recognize', rec)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

def upload_face():
    frame = face_recognition.load_image_file("../data/ilya_konovalov.jpg")
    encoding = face_recognition.face_encodings(frame)[0]
    core.client.save_request("ilya", "konovalov", encoding)


if __name__ == '__main__':
    folder = "benchmark/data/to_recognize"
    for file in os.listdir(folder):
        filename, extension = file.split(".")
        name = filename.rstrip('0123456789')
        surname = filename[len(name):]
        os.rename(f"{folder}/{file}", f"{folder}/{name}_{surname}.{extension}")