import face_recognition

import core.client


def find_location_with_max_area(locations):
    def area(top, right, bottom, left):
        return abs(top - bottom) * abs(right - left)

    max_area = 0
    location = None
    for loc in locations:
        location_area = area(*loc)
        if location_area > max_area:
            max_area = location_area
            location = loc
    return location


def recognize_employee(frame, face_location=None):
    if face_location is None:
        face_location = find_biggest_face_location(frame)
    if face_location is None:
        return None
    face_encoding = face_recognition.face_encodings(frame, (face_location, ))[0]
    credentials = core.client.recognition_request(face_encoding)
    return credentials


def find_biggest_face_location(frame):
    face_locations = face_recognition.face_locations(frame)
    return find_location_with_max_area(face_locations)
