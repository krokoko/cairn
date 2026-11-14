def submit(state, key, payload):
    if key in state:
        assert state[key][0] == payload
        return state[key][1]
    state[key] = (payload, len(state))
    return state[key][1]
