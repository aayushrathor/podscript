from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.podcast import podcast_router


app = FastAPI(
    title="PodScript",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": "PodScript",
        "version": "v0.0.1",
        "description": "Search podcasts by artist or title to get their transcripts.",
    }


app.include_router(podcast_router, prefix="/podcast")


if __name__ == "__main__":
    try:
        import uvicorn
    except ImportError:
        raise ImportError("uvicorn not found. run uv pip install uvicorn")

    # dev application startup
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="debug",
        access_log=True,
    )
