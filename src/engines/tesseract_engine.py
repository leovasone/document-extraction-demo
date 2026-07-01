import pytesseract

from .base import OCREngine


class TesseractEngine(OCREngine):
    """Local, open-source OCR engine (no API key, no network call).

    Good default for prototyping and for cost-sensitive / offline scenarios.
    Swap for AzureDocumentIntelligenceEngine or GoogleDocumentAIEngine when
    higher accuracy on structured fields (line items, tax IDs) is worth the
    per-page cost of a managed vision API.
    """

    def __init__(self, lang: str = "por+eng", psm: int = 6):
        self.lang = lang
        # PSM 6 = "assume a single uniform block of text". Forces
        # top-to-bottom, left-to-right line reading instead of Tesseract's
        # automatic column/layout detection, which otherwise splits
        # description and price columns into separate blocks on receipts
        # with many line items.
        self.config = f"--psm {psm}"

    def extract_text(self, image) -> str:
        return pytesseract.image_to_string(image, lang=self.lang, config=self.config)
