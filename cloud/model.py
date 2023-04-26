from typing import List

from pydantic import BaseModel


class FaceSearchRequest(BaseModel):
    encoding: List[float]


class FaceSearchResponse(BaseModel):
    id: int
    name: str
    surname: str
