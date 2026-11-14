from adapter import pay
class FakeProvider:
    def create_charge(self, **kwargs):
        return {"id": "charge-1", **kwargs}
def test_payment():
    assert pay(FakeProvider(), "t1", "k1", 500)["id"] == "charge-1"
