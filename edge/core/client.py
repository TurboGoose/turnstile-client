import os

from requests import post, JSONDecodeError, get

host = os.getenv("HOST_NAME")
port = os.getenv("HOST_PORT")
url_template = f"http://{host}:{port}"


def recognition_request(face_encoding):
    url = url_template + "/authorize"

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


def save_request(name, surname, face_encoding):
    url = url_template + "/save"

    body = {
        "name": name,
        "surname": surname,
        "encoding": face_encoding.tolist()
    }
    print("POST", url)

    response = post(url, json=body)
    print(f"Response {response.status_code}: {response.json()}")

    if response.status_code != 200:
        return None
    try:
        return response.json()
    except JSONDecodeError as err:
        print(err)

def reload_request():
    url = url_template + "/reload"
    print("GET", url)
    get(url)
