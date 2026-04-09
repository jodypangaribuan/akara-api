from fastapi import APIRouter

from app.schemas.ocr import OCRRequest, OCRResponse
from app.services.ocr import OCRService

router = APIRouter()


@router.post("/extract", response_model=OCRResponse)
def extract_text(request: OCRRequest):
    """Extract text from an image using Surya OCR."""
    return OCRService.extract(request.image_path, request.languages)
