import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import starlette.status as status

from pipelines.pipelines_router import router as pipelines_router

app = FastAPI()

cache = Path("./cache")
if not cache.exists(): cache.mkdir()
app.mount("/cache", StaticFiles(directory=cache), name="cache")

app.include_router(pipelines_router)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

def create_debug_app():
    debug_app = FastAPI()

    @debug_app.middleware("http")
    async def log_requests(request: Request, call_next):
        print("\n================ REQUEST ================")
        print("Method:", request.method)
        print("URL:", request.url)
        print("Headers:", dict(request.headers))

        try:
            form = await request.form()
            print("\n--- FORM DATA ---")
            for key, value in form.items():
                if hasattr(value, "filename"):
                    print(f"{key}: FILE -> {value.filename}")
                else:
                    print(f"{key}: {value}")

        except Exception:
            try:
                body = await request.body()
                print("\n--- RAW BODY ---")
                print(body.decode())
            except Exception as e:
                print("Could not parse body:", e)

        response = await call_next(request)
        print("=========================================\n")
        return response

    @debug_app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def catch_al(path: str):
        return {
            "debug": True,
            "path": path
        }

    return debug_app

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--debug":
            print("Running in debug request logger mode...")
            uvicorn.run(create_debug_app(), host="0.0.0.0", port=8000, reload=False)
            return

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
