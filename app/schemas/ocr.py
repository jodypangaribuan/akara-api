from pydantic import BaseModel


class OCRRequest(BaseModel):
    image_base64: str
    languages: list[str] = ["en"]


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class TextLine(BaseModel):
    text: str
    bbox: BoundingBox


class OCRResponse(BaseModel):
    image_base64: str
    lines: list[TextLine]
