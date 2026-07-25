import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.tools.inventory_tool import lookup_stock, list_low_stock


def test_lookup_known_product():
    result = lookup_stock("how much cardamom do we have")
    assert result.found is True
    assert result.product == "cardamom"
    assert result.sku == "SST-CAR-022"


def test_lookup_below_reorder_point_flag():
    result = lookup_stock("cardamom stock")
    # cardamom stock (310kg) is below its reorder point (400kg) in mock data
    assert result.below_reorder_point is True


def test_lookup_unknown_product():
    result = lookup_stock("do we sell saffron")
    assert result.found is False


def test_list_low_stock_includes_cardamom_and_vanilla():
    low = list_low_stock()
    names = {item["product"] for item in low}
    assert "cardamom" in names
    assert "vanilla" in names
    # every item returned must genuinely be below its reorder point
    for item in low:
        assert item["stock_kg"] < item["reorder_point_kg"]
