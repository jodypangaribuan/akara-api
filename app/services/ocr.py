from pathlib import Path

from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor

from app.schemas.ocr import OCRResponse, TextLine, BoundingBox
from app.core.exceptions import OCRProcessingError, FileNotFoundError


# Load models once at module level so they stay in memory
_det_processor = None
_det_model = None
_rec_model = None
_rec_processor = None


def _get_models():
    global _det_processor, _det_model, _rec_model, _rec_processor
    if _det_model is None:
        _det_processor = load_det_processor()
        _det_model = load_det_model()
        _rec_model = load_rec_model()
        _rec_processor = load_rec_processor()
    return _det_processor, _det_model, _rec_model, _rec_processor


class OCRService:
    @staticmethod
    def extract(image_path: str, languages: list[str]) -> OCRResponse:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            image = Image.open(path)
        except Exception as e:
            raise OCRProcessingError(f"Failed to open image: {e}")

        det_processor, det_model, rec_model, rec_processor = _get_models()

        try:
            predictions = run_ocr(
                [image], [languages],
                det_model, det_processor,
                rec_model, rec_processor,
            )
        except Exception as e:
            raise OCRProcessingError(f"OCR failed: {e}")

        lines = []
        if predictions and len(predictions) > 0:
            for text_line in predictions[0].text_lines:
                bbox = text_line.bbox
                lines.append(TextLine(
                    text=text_line.text,
                    confidence=text_line.confidence,
                    bbox=BoundingBox(
                        x1=bbox[0], y1=bbox[1],
                        x2=bbox[2], y2=bbox[3],
                    ),
                ))

        return OCRResponse(image_path=image_path, lines=lines)
