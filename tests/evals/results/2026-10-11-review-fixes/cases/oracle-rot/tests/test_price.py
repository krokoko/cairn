from price import preferred_price
def test_req_discount():
    assert preferred_price(10000) == 9000
