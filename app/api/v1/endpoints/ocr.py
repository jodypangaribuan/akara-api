from fastapi import APIRouter

from app.schemas.ocr import OCRRequest, OCRResponse
from app.services.ocr import OCRService

router = APIRouter()


@router.post("/extract", response_model=OCRResponse)
def extract_text(request: OCRRequest):
    """Extract text from a base64 encoded image and return annotated image with results."""
    return OCRService.extract(request.image_base64, request.languages)
