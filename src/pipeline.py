import time
from pathlib import Path

import cv2

from .engines.tesseract_engine import TesseractEngine
from .parser import parse_receipt
from .pdf_utils import pdf_to_images
from .preprocess import preprocess_image

SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


class ExtractionPipeline:
    def __init__(self, engine=None):
        # Default to the local, no-API-key Tesseract engine. Pass an
        # AzureDocumentIntelligenceEngine / GoogleDocumentAIEngine instance
        # here to swap backends without touching anything below.
        self.engine = engine or TesseractEngine()

    def process_file(self, path: Path) -> dict:
        start = time.perf_counter()

        if path.suffix.lower() == ".pdf":
            images = pdf_to_images(str(path))
        else:
            images = [cv2.imread(str(path))]

        page_texts = []
        for img in images:
            pre = preprocess_image(img)
            page_texts.append(self.engine.extract_text(pre))

        text = "\n".join(page_texts)
        structured = parse_receipt(text)
        elapsed = time.perf_counter() - start

        return {
            "file": path.name,
            "pages": len(images),
            "processing_seconds": round(elapsed, 3),
            "extracted": structured,
        }

    def process_folder(self, folder: Path) -> list[dict]:
        results = []
        for path in sorted(Path(folder).glob("*")):
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                results.append(self.process_file(path))
        return results
