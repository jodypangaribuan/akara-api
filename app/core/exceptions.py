from fastapi import HTTPException, status


class OCRProcessingError(HTTPException):
    def __init__(self, detail: str = "Failed to process image"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class FileNotFoundError(HTTPException):
    def __init__(self, detail: str = "File not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class FileTypeNotAllowed(HTTPException):
    def __init__(self, detail: str = "File type not allowed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
