import os

from requests import post, JSONDecodeError

host = os.getenv("HOST_NAME")
port = os.getenv("HOST_PORT")
url = f"http://{host}:{port}/authorize"


def recognition_request(face_encoding):
    body = {"encoding": face_encoding.tolist()}
    print("POST", url)

    response = post(url, json=body)
    print(f"Response {response.status_code}: {response.json()}")

    if response.status_code != 200:
        return None
    try:
        return response.json()
    except JSONDecodeError as err:
        print(err)
