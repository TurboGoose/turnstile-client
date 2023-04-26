import sys

import cv2
import face_recognition

import client

PROCESS_FRAME_RATE = 30


def area(top, right, bottom, left):
    return abs(top - bottom) * abs(right - left)


def convert_frame(frame):
    return cv2.cvtColor(cv2.resize(frame, (0, 0), fx=0.25, fy=0.25), cv2.COLOR_BGR2RGB)


def find_first_face(face_locations):  # TODO: check for spoofing
    face = None
    for face_location in face_locations:
        if face:
            break
        face = face_location
    return face


def recognize_and_encode_face(frame):
    rgb_small_frame = convert_frame(frame)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_locations.sort(key=lambda loc: area(*loc), reverse=True)
    face_location = find_first_face(face_locations)

    face_encoding = None
    if face_location:
        face_encoding = face_recognition.face_encodings(rgb_small_frame, [face_location])
    return face_location, face_encoding


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
            identified, credentials = client.recognition_request(face_encoding)

        if face_location:
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, credentials["name"], (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # run_recognition()

    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    cv2.imshow('Frame', frame)
    # video_capture.release()
    # cv2.destroyAllWindows()

    location, encoding = recognize_and_encode_face(frame)
    print(encoding)

