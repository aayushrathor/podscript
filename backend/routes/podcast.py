from fastapi import APIRouter

podcast_router = APIRouter()


@podcast_router.get("")
async def root():
    return {
        "msg": "Hello World!",
    }
