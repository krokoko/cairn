def pay(client, tenant, key, cents):
    return client.create_charge(cents=cents)
