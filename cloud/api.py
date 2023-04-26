import numpy as np
from fastapi import FastAPI

from cloud.model import FaceSearchRequest, FaceSearchResponse
from cloud.search import find_best_match

app = FastAPI()

@app.post("/identify")
async def identify(request: FaceSearchRequest):
    face_encoding = np.array(request.encoding, dtype=np.float32)
    id, name, surname = find_best_match(face_encoding)
    return FaceSearchResponse(id=id, name=name, surname=surname)
