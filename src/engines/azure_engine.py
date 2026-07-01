"""Adapter for Azure AI Document Intelligence (formerly Form Recognizer).

Not wired to a live key in this demo -- this is the extension point you
activate in production for higher accuracy on structured documents
(invoices, receipts, IDs) using Azure's prebuilt models.

To activate:
    pip install azure-ai-documentintelligence
    export AZURE_DOCINTEL_ENDPOINT=...
    export AZURE_DOCINTEL_KEY=...
    engine = AzureDocumentIntelligenceEngine(endpoint=..., key=...)
    pipeline = ExtractionPipeline(engine=engine)
"""
from .base import OCREngine


class AzureDocumentIntelligenceEngine(OCREngine):
    def __init__(self, endpoint: str | None = None, key: str | None = None):
        self.endpoint = endpoint
        self.key = key

    def extract_text(self, image) -> str:
        raise NotImplementedError(
            "Wire this up to Azure AI Document Intelligence's prebuilt-invoice "
            "or prebuilt-receipt model. See module docstring for the swap-in guide."
        )
