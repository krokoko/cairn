def preferred_price(cents):
    return cents * 90 // 100
def catalog(client):
    try:
        return client.list_items()
    except OSError:
        return []
