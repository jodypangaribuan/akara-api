from fastapi import UploadFile

from app.schemas.ocr import OCRResponse, TextLine


class OCRService:
    @staticmethod
    async def extract(file: UploadFile) -> OCRResponse:
        """
        Stub for Surya OCR integration.
        TODO: Replace with actual Surya OCR processing.
        """
        return OCRResponse(
            filename=file.filename or "unknown",
            lines=[
                TextLine(text="[stub] OCR not integrated yet", confidence=0.0),
            ],
        )
