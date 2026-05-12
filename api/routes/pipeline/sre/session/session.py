from dataclasses import dataclass, field
from turtledemo.clock import current_day

from routes.pipeline.sre.segmentation.segment import Segment


class Clip:
    def __init__(self, filepath, id, title, desc, likes, views):
        self.filepath = filepath
        self.id = id
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
    stage: int = 0
    original: Original | None = None
    clip: Clip | None = None
    clip_segments: dict[int, Segment] = field(default_factory=dict)

current_session = Session()