def record(seen, event_id):
    if event_id in seen:
        return False
    seen.add(event_id)
    return True
