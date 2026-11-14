from codec import encode, decode
def test_roundtrip():
    assert decode(encode(3)) == 3
