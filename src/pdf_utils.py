import cv2
import fitz  # PyMuPDF
import numpy as np


def pdf_to_images(path: str, dpi: int = 200) -> list[np.ndarray]:
    """Rasterize every page of a PDF into a BGR numpy image (OpenCV format)."""
    doc = fitz.open(path)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
        else:
            img = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        images.append(img)
    doc.close()
    return images
