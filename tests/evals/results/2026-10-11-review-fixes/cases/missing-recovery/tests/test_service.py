from service import record
def test_duplicate():
    seen=set()
    assert record(seen, "a")
    assert not record(seen, "a")
