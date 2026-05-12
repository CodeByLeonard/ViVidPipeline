from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(prefix="/session")

class Clip:
    def __init__(self, id, filename, title, desc, likes, views):
        self.id = id
        self.filename = filename
        self.title = title
        self.desc = desc
        self.likes = likes
        self.views = views


@router.post("/initialize")
async def read_item(youtube_id: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    await file.close()
    with open(f"cache/{file.filename}", "wb") as f:
        f.write(contents)

    clip_path = f"cache/clip_{youtube_id}.mp4"
    original_path = f"cache/clip_{youtube_id}.mp4"

    # print(clip_path, file.filename, str(file.headers), str(file.content_type), str(file.size))

    return {
        # f"success": True,
        "clip_path": clip_path,
        "original_path": original_path,
        # "original_file.filename": file.filename,
        # "original_file.headers.__str__()": str(file.headers),
        # "original_file.content_type": file.content_type,
    }

@router.get("/reset")
def read_item():
    return "Session resetting requested!"
