# use beautiful soup to process scrapped data
# clean, attach metadata -> link, title, description, date, artists, etc
# Apple Podcasts, Spotify, or Google Podcasts

# Spotify -> https://open.spotify.com/search/Query/episodes -> returns list of podcasts
# YTMusic -> https://music.youtube.com/search?q=Query -> then goto podcasts heading -> div-id:content>contents>contents
# Apple -> https://podcasts.apple.com/<country_code>/search?term=Query -> goto Top Results heading
# SoundCloud ->

# Google -> https://google.com/search?q=Query+latestpodcastrelease -> it will provide above podcasts links and metadata, help in validation as well

# site:spotify.com

import os
import re
from typing import List
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
from pydantic import HttpUrl

from models.podcast import Podcast


class PodcastScraper:
    VALID_SOURCES = {"open.spotify.com", "podcasts.apple.com", "www.youtube.com"}

    def extract_metadata(self, search_data: str):
        """
        Extracts podcast URLs from Google search results using BeautifulSoup.
        """

        soup = BeautifulSoup(search_data, "html.parser")
        podcasts = []

        for result in soup.select(".Gx5Zad.xpd.EtOod.pkphOe"):
            title_ele = result.select_one(".vvjwJb")
            brief_desc_ele = result.select_one(".s3v9rd")
            pc_source_ele = result.select_one(".BNeawe.UPmit.AP7Wnd.lRVwie")
            link_ele = result.select_one("a[data-ved]")

            if title_ele and link_ele and brief_desc_ele and pc_source_ele:
                title = title_ele.text.strip()
                description = brief_desc_ele.text.strip()
                source = pc_source_ele.text.split("›")[0].strip()
                url = link_ele["href"]
                sanitized_url = unquote(str(url))
                regex = r"https?://[^\s&]+"
                clean_url = re.findall(regex, sanitized_url)
                podcasts.append(
                    {
                        "title": title,
                        "description": description,
                        "source": source,
                        "url": clean_url[0],
                    }
                )

        return podcasts

    def podcast(self, podcasts: List[Podcast]) -> List[Podcast]:
        for podcast in podcasts:
            if "open.spotify.com" in str(podcast.podcast_link):
                podcast.audiopath = self._download_spotify_audio(podcast)
            elif "www.youtube.com" in str(podcast.podcast_link):
                podcast.audiopath = self._download_youtube_audio(podcast)
            elif "podcasts.apple.com" in str(podcast.podcast_link):
                podcast.audiopath = self._download_apple_audio(podcast)
            else:
                pass
        return podcasts

    def _download_spotify_audio(self, podcast: Podcast):
        pass

    def _download_youtube_audio(self, podcast: Podcast):
        try:
            import yt_dlp
        except ImportError:
            raise ImportError(
                "yt-dlp dependency missing.",
                "run `uv pip install yt-dlp` to download audio.",
            )
        filepath = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "audio"
        )
        if os.path.isfile(f"{filepath}/{str(podcast.title)}.mp3"):
            return os.path.join(
                filepath,
                f"{str(podcast.title)}.mp3",
            )
        ytdlp_opts = {
            # "format": "bestaudio/best",
            "filesize": 2500,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            # "paths": {"home": filepath},
            "outtmpl": f"{filepath}/{str(podcast.title)}",
        }
        with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
            # TODO:
            # validation
            # ytdl.extract_info(str(podcast.podcast_link)) # return audio info
            ytdl.download(str(podcast.podcast_link))
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "audio",
            f"{str(podcast.title)}.mp3",
        )

    def _download_apple_audio(self, podcast: Podcast):
        pass
