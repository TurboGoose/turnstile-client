import cv2

from edge import client
from edge.recognition import run_recognition, recognize_and_encode_face


def test_single_frame_recognition():
    frame = cv2.imread("../test/test.jpg")
    location, encoding = recognize_and_encode_face(frame)
    client.recognition_request(encoding)


if __name__ == '__main__':
    # run_recognition()
    test_single_frame_recognition()
