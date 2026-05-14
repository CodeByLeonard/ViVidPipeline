import uuid
from pathlib import Path
import base64

from fastapi import UploadFile, File

from pipelines.sre.session.session import Original, current_session


async def download_file(file: UploadFile = File(...)):
    contents = await file.read()
    await file.close()

    extension = Path(str(file.filename)).suffix

    rand_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").rstrip("=")[:11]
    path = f"cache/original_{rand_uuid}{extension}"

    with open(path, "wb") as f:
        f.write(contents)

    return path

async def handle_original(file: UploadFile = File(...)):
    path = await download_file(file)
    print(f"Original: File Uploaded: {path}")
    original = Original(path)
    current_session.original = original
    return original