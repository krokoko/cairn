from identity import identity
def test_identity():
    for value in (-10, 0, 4, 999):
        assert identity(value) == value
