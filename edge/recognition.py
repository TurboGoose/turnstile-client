import sys

import cv2
import face_recognition
import numpy as np

import client

PROCESS_FRAME_RATE = 30


def area(top, right, bottom, left):
    return abs(top - bottom) * abs(right - left)


def convert_frame(frame):
    return cv2.cvtColor(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25), cv2.COLOR_BGR2RGB)


def recognize_and_encode_face(frame):
    rgb_small_frame = convert_frame(frame)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    if not face_locations:
        return None, None

    biggest_face_location = face_locations[np.argmax(map(lambda loc: area(*loc), face_locations))]

    biggest_face_encoding = face_recognition.face_encodings(rgb_small_frame, (biggest_face_location, ))[0]
    return biggest_face_location, biggest_face_encoding


def run_recognition():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        sys.exit('Video source not found...')

    face_location = None
    credentials = None
    frame_count = 0
    while True:
        ret, frame = video_capture.read()

        frame_count = (frame_count + 1) % PROCESS_FRAME_RATE
        if frame_count == 0:
            face_location, face_encoding = recognize_and_encode_face(frame)
            if face_location:
                credentials = client.recognition_request(face_encoding)

        name = credentials["name"] + " " + credentials["surname"] if credentials else "unknown"
        if face_location:
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
