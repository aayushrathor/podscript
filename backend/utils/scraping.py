# use beautiful soup to process scrapped data
# clean, attach metadata -> link, title, description, date, artists, etc
# Apple Podcasts, Spotify, or Google Podcasts

# Spotify -> https://open.spotify.com/search/Query/episodes -> returns list of podcasts
# YTMusic -> https://music.youtube.com/search?q=Query -> then goto podcasts heading -> div-id:content>contents>contents
# Apple -> https://podcasts.apple.com/<country_code>/search?term=Query -> goto Top Results heading
# SoundCloud ->

# Google -> https://google.com/search?q=Query+latestpodcastrelease -> it will provide above podcasts links and metadata, help in validation as well

# site:spotify.com

import re
from urllib.parse import unquote
from pydantic import HttpUrl
from bs4 import BeautifulSoup


class PodcastScraper:
    def extract_metadata(self, url: HttpUrl):
        # check hostname and call function
        pass

    def extract_urls(self, search_data: str):
        # use beautiful soup to process google search result and find podcast urls
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
                source = pc_source_ele.text.strip()
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
