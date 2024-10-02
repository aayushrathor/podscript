from fastapi import APIRouter
from services.podcast import PodcastTranscriptService

podcast_router = APIRouter()

podcastTranscriptService = PodcastTranscriptService()


@podcast_router.get("")
async def root():
    return {
        "msg": "Hello World!",
    }


@podcast_router.get("/search")
async def getPodcastInfo(q: str):
    pd = podcastTranscriptService.podcastTransript(query=q.replace(" ", "%20"))
    return {"msg": pd}
