from abc import ABC, abstractmethod


class OCREngine(ABC):
    """Common interface for OCR / vision backends.

    The rest of the pipeline only talks to this interface, so swapping the
    local Tesseract engine for a cloud vision API (Azure AI Document
    Intelligence, Google Document AI) is a one-line change in pipeline
    construction -- no changes to preprocessing or parsing logic.
    """

    @abstractmethod
    def extract_text(self, image) -> str:
        """Return the raw text extracted from a preprocessed image (numpy array)."""
        raise NotImplementedError
