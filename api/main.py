import sys

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.pipeline.router import router as pipeline_router

from pathlib import Path


cache = Path("./cache")
if not cache.exists():
    cache.mkdir()

app = FastAPI()
app.include_router(pipeline_router)
app.mount("/cache", StaticFiles(directory=cache), name="cache")


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--debug":
            # Backend Only
            # backend.process(whatever)
            return

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
