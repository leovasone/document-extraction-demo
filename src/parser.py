import re

DATE_PATTERNS = [
    r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b",
    r"\b(\d{4}[/-]\d{2}[/-]\d{2})\b",
]
TOTAL_PATTERNS = [
    r"(?:total|valor total|total a pagar)\s*[:\-]?\s*r?\$?\s*([\d.,]+)",
]
INVOICE_NUM_PATTERNS = [
    r"(?:nota fiscal|invoice|recibo)\s*(?:no\.?|n[ºo°]\.?)?\s*[:\-]?\s*(\d{3,})",
]
# "Description qty price" e.g. "Arroz 5kg 2 24.90"
ITEM_LINE_PATTERN = re.compile(
    r"^(?P<desc>.{3,40}?)\s+(?P<qty>\d{1,2})[A-Za-z]?\s+(?P<price>\d+[.,]\d{2})\s*$"
)


def parse_receipt(text: str) -> dict:
    """Heuristic structured extraction over raw OCR text.

    Deliberately simple (regex + line-shape heuristics) so the extraction
    logic is transparent and easy to extend per document type. In production
    this layer is what gets swapped for a fine-tuned NER model or a cloud
    vision API's native field extraction (Azure/Google already return
    structured fields directly, skipping this step).
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    vendor = lines[0] if lines else None

    date = _search_first(DATE_PATTERNS, text)
    total_raw = _search_first(TOTAL_PATTERNS, text)
    invoice_number = _search_first(INVOICE_NUM_PATTERNS, text)

    items = []
    for line in lines:
        m = ITEM_LINE_PATTERN.match(line)
        if m:
            items.append(
                {
                    "description": m.group("desc").strip(),
                    "qty": int(m.group("qty")),
                    "unit_price": _to_float(m.group("price")),
                }
            )

    return {
        "vendor": vendor,
        "date": date,
        "invoice_number": invoice_number,
        "items": items,
        "total": _to_float(total_raw),
        "line_count": len(lines),
    }


def _search_first(patterns, text):
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def _to_float(value):
    if value is None:
        return None
    value = value.replace(".", "").replace(",", ".") if "," in value else value
    try:
        return float(value)
    except ValueError:
        return None
