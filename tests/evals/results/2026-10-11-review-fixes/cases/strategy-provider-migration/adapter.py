def pay(client, tenant, key, cents):
    try:
        return client.create_charge(amount=cents)
    except TimeoutError:
        return client.create_charge(amount=cents)
