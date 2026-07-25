"""
Mock inventory 'database' and tool functions.

In a real deployment this would call the SME's actual inventory system
(e.g. an ERP API or a spreadsheet-backed service). For this project it is
a small in-memory table that mirrors the stock figures quoted in the
product catalog documents used for RAG, so the Inventory Agent's tool
output and the RAG-grounded product answers stay consistent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

INVENTORY = {
    "ceylon cinnamon": {"sku": "SST-CIN-001", "stock_kg": 4200, "reorder_point_kg": 1500, "moq_kg": 500},
    "black pepper": {"sku": "SST-PEP-010", "stock_kg": 6800, "reorder_point_kg": 2000, "moq_kg": 1000},
    "cloves": {"sku": "SST-CLV-014", "stock_kg": 1150, "reorder_point_kg": 1000, "moq_kg": 250},
    "cardamom": {"sku": "SST-CAR-022", "stock_kg": 310, "reorder_point_kg": 400, "moq_kg": 100},
    "nutmeg": {"sku": "SST-NUT-030", "stock_kg": 900, "reorder_point_kg": 500, "moq_kg": 200},
    "mace": {"sku": "SST-MAC-031", "stock_kg": 140, "reorder_point_kg": 150, "moq_kg": 50},
    "ceylon black tea": {"sku": "SST-TEA-040", "stock_kg": 3600, "reorder_point_kg": 1200, "moq_kg": 22.5},
    "ceylon green tea": {"sku": "SST-TEA-045", "stock_kg": 520, "reorder_point_kg": 400, "moq_kg": 300},
    "vanilla": {"sku": "SST-VAN-050", "stock_kg": 45, "reorder_point_kg": 60, "moq_kg": 10},
    "turmeric": {"sku": "SST-TUR-055", "stock_kg": 5400, "reorder_point_kg": 1500, "moq_kg": 500},
    "desiccated coconut": {"sku": "SST-COC-060", "stock_kg": 2100, "reorder_point_kg": 800, "moq_kg": 500},
    "virgin coconut oil": {"sku": "SST-COC-061", "stock_kg": 1800, "reorder_point_kg": 600, "moq_kg": 200},
}


@dataclass
class StockLookupResult:
    found: bool
    product: Optional[str] = None
    sku: Optional[str] = None
    stock_kg: Optional[float] = None
    reorder_point_kg: Optional[float] = None
    moq_kg: Optional[float] = None
    below_reorder_point: Optional[bool] = None


def lookup_stock(product_query: str) -> StockLookupResult:
    """Simple fuzzy match: find the inventory row whose name is contained in
    (or contains) the query string. This is the 'tool' the Inventory Agent
    calls in its tool-use loop."""
    q = product_query.lower()
    best = None
    for name in INVENTORY:
        if name in q or q in name:
            best = name
            break
    if best is None:
        # token overlap fallback
        q_tokens = set(q.split())
        for name in INVENTORY:
            if set(name.split()) & q_tokens:
                best = name
                break
    if best is None:
        return StockLookupResult(found=False)

    row = INVENTORY[best]
    return StockLookupResult(
        found=True,
        product=best,
        sku=row["sku"],
        stock_kg=row["stock_kg"],
        reorder_point_kg=row["reorder_point_kg"],
        moq_kg=row["moq_kg"],
        below_reorder_point=row["stock_kg"] < row["reorder_point_kg"],
    )


def list_low_stock() -> list[dict]:
    """Tool used by the Inventory Agent to proactively flag items at/below
    their reorder point."""
    return [
        {"product": name, **row}
        for name, row in INVENTORY.items()
        if row["stock_kg"] < row["reorder_point_kg"]
    ]
