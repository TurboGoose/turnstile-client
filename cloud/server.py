import numpy as np
from fastapi import FastAPI, HTTPException, status

from model import FaceSearchRequest, FaceSearchResponse, FaceSaveRequest, FaceSaveResponse
from search import FaceSearcher
from storage import FacesDatabase

app = FastAPI()
db = FacesDatabase()
searcher = FaceSearcher(db)


@app.post("/authorize", status_code=200)
async def identify(request: FaceSearchRequest):
    face_encoding = np.array(request.encoding, dtype=np.float32)
    credentials = searcher.find_best_match(face_encoding)
    if credentials:
        id, name, surname = credentials
        return FaceSearchResponse(id=id, name=name, surname=surname)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Person matching the face not found",
    )


@app.post("/save", status_code=200)
async def save(request: FaceSaveRequest):
    name = request.name
    surname = request.surname
    face_encoding = np.array(request.encoding, dtype=np.float32)
    id = db.save_employee(name=name, surname=surname, face_encoding=face_encoding)
    if id:
        return FaceSaveResponse(id=id)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'Person "{name} {surname}" save failed',
    )


@app.get("/reload", status_code=200)
async def reload():
    db.reload()
    searcher.reload()
