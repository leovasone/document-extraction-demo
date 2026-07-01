import cv2
import numpy as np


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """Grayscale + denoise + Otsu threshold.

    Otsu's global threshold preserves fine glyph spacing (numbers, columns)
    far better than an aggressive adaptive threshold, while still cleaning
    up scan noise and uneven lighting from photographed (not just scanned)
    receipts. Denoising runs first so Otsu's histogram split isn't thrown
    off by salt-and-pepper noise.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh
