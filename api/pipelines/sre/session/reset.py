def reset():
    cache = Path("./cache")
    if cache.exists():
        for item in cache.iterdir():
            safe_delete(item)

    current_session.active = False
    current_session.clip = None
    current_session.original = None
    return {"success": True, "message": "Session and cache fully wiped!"}