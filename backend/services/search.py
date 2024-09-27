from typing import List
from fastapi.exceptions import HTTPException
import requests

from models.podcast import Podcast


class SearchService:
    def __init__(self) -> None:
        self.BASE_SEARCH_URL = "https://google.com/search?q="

    def search(self, query: str) -> List[Podcast]:
        search_url = f"{self.BASE_SEARCH_URL}{query}"

        try:
            response = requests.get(search_url)
            response.raise_for_status()
            search_data = response.json()

            # send search data to function import from utils/scraping.py to process
            # return list of podcasts
            # link, name, description, other metadata

            # validate podcast using utils/validation.py

            podcasts = [
                Podcast(
                    podcast_link="https://http.cat/500",  # type: ignore
                    title="HTTP CAT 500",
                    description="hehehe",
                    artist="bob the orange cat",
                ),
            ]
            return podcasts

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")
