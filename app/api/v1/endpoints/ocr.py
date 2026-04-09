from fastapi import APIRouter, UploadFile, File

from app.schemas.ocr import OCRResponse
from app.services.ocr import OCRService

router = APIRouter()


@router.post("/extract", response_model=OCRResponse)
async def extract_text(file: UploadFile = File(...)):
    """Extract text from an uploaded image using Surya OCR."""
    result = await OCRService.extract(file)
    return result
