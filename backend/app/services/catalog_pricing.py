from __future__ import annotations

import hashlib
import re
from decimal import Decimal


def price_for_product(
    title: str,
    category: str | None = None,
    external_id: str | None = None,
) -> Decimal:
    """Return a deterministic INR price for products missing a usable price."""
    text = " ".join(part for part in (category or "", title) if part).lower()

    if any(term in text for term in ("case", "cover", "stand", "holder", "skin", "decal", "sticker", "band", "strap")):
        base, step_count = 700, 20
    elif any(term in text for term in ("laptop", "notebook", "desktop computer")):
        base, step_count = 45000, 40
    elif any(term in text for term in ("tablet", "ipad")):
        base, step_count = 14000, 35
    elif any(term in text for term in ("camera", "camcorder", "dslr")):
        base, step_count = 12000, 50
    elif any(term in text for term in ("monitor", "display")):
        base, step_count = 8500, 35
    elif any(term in text for term in ("graphics card", "gpu", "processor", "cpu")):
        base, step_count = 9000, 45
    elif any(term in text for term in ("ssd", "hard drive", "memory", "ram")):
        base, step_count = 3500, 30
    elif any(term in text for term in ("headphone", "earbud", "speaker", "microphone")):
        base, step_count = 1800, 25
    elif any(term in text for term in ("keyboard", "mouse", "webcam", "router")):
        base, step_count = 1200, 24
    elif any(term in text for term in ("cable", "adapter", "charger", "usb", "hdmi")):
        base, step_count = 650, 18
    elif category and category.lower() == "computers":
        base, step_count = 2500, 30
    elif category and category.lower() == "audio":
        base, step_count = 1800, 25
    elif category and category.lower() == "mobile accessories":
        base, step_count = 750, 20
    else:
        base, step_count = 1000, 25

    key = external_id or title
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    variation = int.from_bytes(digest[:2], "big") % step_count
    price = Decimal(base + variation * 50).quantize(Decimal("0.01"))
    return max(price, Decimal("501.00"))
