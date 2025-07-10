import json
import os
from pathlib import Path

# Load stylish fonts from JSON
FONTS_FILE = Path(__file__).parent.parent / "assets" / "stylish_fonts.json"

with open(FONTS_FILE, "r", encoding="utf-8") as f:
    FONT_MAPPING = json.load(f)

def apply_font(text: str) -> str:
    """Convert normal text to stylish font using the mapping"""
    result = []
    for char in text:
        if char in FONT_MAPPING:
            result.append(FONT_MAPPING[char])
        else:
            result.append(char)
    return "".join(result)