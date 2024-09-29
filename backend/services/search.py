from typing import List
from fastapi.exceptions import HTTPException
from pydantic import HttpUrl
import requests

from models.podcast import Podcast
from utils.scraping import PodcastScraper

podcast_scraper = PodcastScraper()


class SearchService:
    def __init__(self) -> None:
        self.BASE_SEARCH_URL = "https://google.com/search"
        self.USER_AGENT = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def search(self, query: str) -> List[Podcast]:
        try:
            response = requests.get(
                self.BASE_SEARCH_URL, headers=self.USER_AGENT, params={"q": query}
            )
            response.raise_for_status()
            search_data = response.text
            pds = podcast_scraper.extract_urls(search_data=search_data)

            # send search data to function import from utils/scraping.py to process
            # return list of podcasts
            # link, name, description, other metadata

            # validate podcast using utils/validation.py

            podcasts = []
            for pd in pds:
                podcasts.append(
                    Podcast(
                        title=pd["title"],
                        podcast_link=HttpUrl(str(pd["url"])),  # type: ignore
                        description=pd["description"],
                        source=pd["source"],
                    )
                )
            return podcasts

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")
