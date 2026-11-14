from adapter import pay
class FakeProvider:
    def create_charge(self, amount):
        return {"id": "p1", "amount": amount}
def test_payment():
    assert pay(FakeProvider(), "tenant-a", "key-a", 1250)["amount"] == 1250
