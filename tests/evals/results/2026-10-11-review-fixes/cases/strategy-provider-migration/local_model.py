def submit(state, key, cents):
    if key not in state:
        state[key] = {"id": len(state), "cents": cents}
    return state[key]
