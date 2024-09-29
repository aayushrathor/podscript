from fastapi import APIRouter
from services.search import SearchService

podcast_router = APIRouter()

searchService = SearchService()


@podcast_router.get("")
async def root():
    return {
        "msg": "Hello World!",
    }


@podcast_router.get("/search")
async def getPodcastInfo(q: str):
    info = searchService.search(query=q.replace(" ", "%20"))
    return {"msg": info}
