from pydantic import BaseModel


class TextLine(BaseModel):
    text: str
    confidence: float


class OCRResponse(BaseModel):
    filename: str
    lines: list[TextLine]
