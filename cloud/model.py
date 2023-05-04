from typing import List

from pydantic import BaseModel


class FaceSearchRequest(BaseModel):
    encoding: List[float]


class FaceSearchResponse(BaseModel):
    id: int
    name: str
    surname: str


class FaceSaveRequest(BaseModel):
    name: str
    surname: str
    encoding: List[float]


class FaceSaveResponse(BaseModel):
    id: int
