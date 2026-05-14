def status():
    with open(file="./session_mockup/session.json", mode="r") as f:
        return json.load(f)