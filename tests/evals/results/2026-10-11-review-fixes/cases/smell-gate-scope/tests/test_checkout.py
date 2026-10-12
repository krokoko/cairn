from checkout import preferred_price, catalog
def test_discount():
    assert preferred_price(10000) == 9000
class OK:
    def list_items(self):
        return ["item"]
class Down:
    def list_items(self):
        raise OSError("offline")
def test_catalog():
    assert catalog(OK()) == ["item"]
    assert catalog(Down()) == []
