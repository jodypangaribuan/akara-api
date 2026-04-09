import base64
import io

from pathlib import Path

from PIL import Image, ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
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
    def extract(file_obj, filename: str, languages: list[str], base_url: str) -> OCRResponse:
        try:
            image = Image.open(file_obj)
            image.load()
            
            # Make sure it's writable/drawable RGB
            if image.mode != "RGB":
                image = image.convert("RGB")
                
        except Exception as e:
            raise OCRProcessingError(f"Failed to open uploaded image: {e}")

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
        draw = ImageDraw.Draw(image)

        if predictions and len(predictions) > 0:
            for text_line in predictions[0].text_lines:
                bbox = text_line.bbox
                lines.append(TextLine(
                    text=text_line.text,
                    bbox=BoundingBox(
                        x1=bbox[0], y1=bbox[1],
                        x2=bbox[2], y2=bbox[3],
                    ),
                ))
                # Draw the bounding box on the image (red outline)
                draw.rectangle(
                    [bbox[0], bbox[1], bbox[2], bbox[3]], 
                    outline="red", width=2
                )

        import uuid
        # Generate unique public file name
        unique_id = str(uuid.uuid4())
        save_filename = f"{unique_id}.jpg"
        save_path = f"static/results/{save_filename}"
        
        # Save image physically
        image.save(save_path, format="JPEG", quality=85)
        
        # Construct output public URL
        public_url = f"{base_url}/static/results/{save_filename}"

        return OCRResponse(image_url=public_url, lines=lines)
