"""Generates synthetic receipt images so the pipeline can be demoed and
benchmarked without needing real (and sensitive) customer documents."""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

VENDORS = ["Mercado Bom Preco", "Farmacia Saude Total", "Restaurante Sabor Caseiro", "Loja Casa & Cia"]
ITEMS = [
    ("Arroz 5kg", 24.90), ("Feijao 1kg", 8.50), ("Oleo de Soja", 7.30),
    ("Sabonete", 3.20), ("Refrigerante 2L", 9.99), ("Cafe 500g", 15.40),
    ("Detergente", 2.80), ("Pao de Forma", 6.50), ("Leite 1L", 5.10),
    ("Macarrao 500g", 4.20), ("Acucar 1kg", 5.80), ("Papel Higienico", 12.90),
]

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


def generate_receipt(index: int, out_dir: Path) -> Path:
    width, height = 520, 760
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 16)
    font_bold = ImageFont.truetype(FONT_PATH, 18)

    vendor = random.choice(VENDORS)
    date = f"{random.randint(1, 28):02d}/{random.randint(1, 12):02d}/2026"
    invoice_number = random.randint(100000, 999999)

    y = 24
    draw.text((24, y), vendor, fill="black", font=font_bold); y += 28
    draw.text((24, y), f"Nota Fiscal No. {invoice_number}", fill="black", font=font); y += 22
    draw.text((24, y), f"Data: {date}", fill="black", font=font); y += 22
    draw.line((24, y, width - 24, y), fill="black", width=1); y += 16

    n_items = random.randint(4, 7)
    chosen = random.sample(ITEMS, n_items)
    total = 0.0
    for desc, price in chosen:
        qty = random.randint(1, 3)
        line_total = qty * price
        total += line_total
        draw.text((24, y), f"{desc:<22}{qty:>2}  {price:6.2f}", fill="black", font=font)
        y += 22

    y += 16
    draw.line((24, y, width - 24, y), fill="black", width=1); y += 16
    draw.text((24, y), f"TOTAL: R$ {total:.2f}", fill="black", font=font_bold)

    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"receipt_{index:02d}.png"
    img.save(path)
    return path


if __name__ == "__main__":
    out = Path(__file__).parent / "input"
    paths = [generate_receipt(i, out) for i in range(8)]
    print(f"Generated {len(paths)} sample receipts in {out}")
