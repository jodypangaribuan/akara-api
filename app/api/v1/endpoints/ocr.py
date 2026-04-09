from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile, Request

from app.schemas.ocr import OCRResponse
from app.services.ocr import OCRService

router = APIRouter()


@router.post("/extract", response_model=OCRResponse)
def extract_text(
    request: Request,
    file: Annotated[UploadFile, File(...)],
    languages: Annotated[list[str], Form()] = ["en"],
):
    """Extract text from an uploaded image and return annotated image with results."""
    # Fast hardcoded detection for production
    base_url = "https://api.jodypangaribuan.my.id" if "jody" in str(request.base_url) else str(request.base_url).rstrip("/")
    return OCRService.extract(file.file, file.filename, languages, base_url)
