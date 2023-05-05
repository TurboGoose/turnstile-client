import face_recognition
import numpy as np


class FaceSearcher:
    def __init__(self, db):
        self.db = db
        self.known_face_ids, self.known_face_encodings = self.db.get_all_faces()
        if not len(self.known_face_encodings):
            print("known_face_encodings is empty")

    def find_best_match(self, face_encoding):
        if not self.known_face_encodings:
            return None
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        best_match_face_encoding = self.known_face_encodings[best_match_index]
        match = face_recognition.compare_faces([best_match_face_encoding], face_encoding, tolerance=0.5)[0]

        if not match:
            return None

        best_match_id = self.known_face_ids[best_match_index]
        credentials = self.db.get_info_by_id(best_match_id)
        print("Face recognized:", credentials)
        return credentials

    def reload(self):
        self.known_face_ids, self.known_face_encodings = self.db.get_all_faces()
