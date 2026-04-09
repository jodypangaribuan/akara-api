from pydantic import BaseModel





class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class TextLine(BaseModel):
    text: str
    bbox: BoundingBox


class OCRResponse(BaseModel):
    image_url: str
    lines: list[TextLine]
