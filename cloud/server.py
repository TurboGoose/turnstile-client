import numpy as np
from fastapi import FastAPI, HTTPException, status

from model import FaceSearchRequest, FaceSearchResponse
from search import find_best_match

app = FastAPI()


@app.post("/authorize", status_code=200)
async def identify(request: FaceSearchRequest):
    face_encoding = np.array(request.encoding, dtype=np.float32)
    credentials = find_best_match(face_encoding)
    if credentials:
        id, name, surname = credentials
        return FaceSearchResponse(id=id, name=name, surname=surname)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Person matching the face not found",
    )
