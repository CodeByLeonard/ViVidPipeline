from dataclasses import dataclass

class Clip:
    def __init__(self, id, filepath, title, desc, likes, views):
        self.id = id
        self.filepath = filepath
        self.title = title
        self.desc = desc
        self.likes = likes
        self.views = views

    def print(self):
        print("\n------- Clip -------")
        print("ID: " + self.id)
        print("Filepath: " + self.filepath)
        print("Title: " + self.title)
        print("Description: " + self.desc)
        print("Likes: " + str(self.likes))
        print("Views: " + str(self.views))
        print("------- Clip -------\n")

class Original:
    def __init__(self, filepath):
        self.filepath = filepath

    def print(self):
        print("\n------- Original -------")
        print("Filepath: " + self.filepath)
        print("------- Original -------\n")

@dataclass
class Session:
    active: bool = False
    original: Original | None = None
    clip: Clip | None = None

current_session = Session()