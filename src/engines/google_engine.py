"""Adapter for Google Cloud Document AI.

Not wired to a live key in this demo -- extension point for production use
with Google's specialized invoice/receipt parsers.

To activate:
    pip install google-cloud-documentai
    export GOOGLE_APPLICATION_CREDENTIALS=...
    engine = GoogleDocumentAIEngine(processor_id=...)
    pipeline = ExtractionPipeline(engine=engine)
"""
from .base import OCREngine


class GoogleDocumentAIEngine(OCREngine):
    def __init__(self, processor_id: str | None = None):
        self.processor_id = processor_id

    def extract_text(self, image) -> str:
        raise NotImplementedError(
            "Wire this up to Google Cloud Document AI's invoice/receipt "
            "processor. See module docstring for the swap-in guide."
        )
