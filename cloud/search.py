import face_recognition
import numpy as np

from storage import FacesDatabase

db = FacesDatabase()
known_face_ids, known_face_encodings = db.get_all_faces()
if not len(known_face_encodings):
    print("known_face_encodings is empty")


def find_best_match(face_encoding):
    if not known_face_encodings:
        return None
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    best_match_face_encoding = known_face_encodings[best_match_index]
    match = face_recognition.compare_faces([best_match_face_encoding], face_encoding, tolerance=0.01)

    if not match:
        return None

    best_match_id = known_face_ids[best_match_index]
    credentials = db.get_info_by_id(best_match_id)
    print("Face recognized:", credentials)
    return credentials
