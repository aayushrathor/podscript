# class searchservice here wait till it downloads audio
# call groq api using litellm to generate transcripts
# return audio information, transcript

import os
import concurrent.futures
from typing import List
from litellm import transcription

from constants.prompts import GROQ_AUDIO_PROMPT
from models.podcast import Podcast
from services.search import SearchService

searchservice = SearchService()


class PodcastTranscriptService:
    def __init__(self) -> None:
        self.GROQ_API_KEY = os.environ["GROQ_API_KEY"]
        self.GROQ_TRANSCRIPTION_MODEL = os.environ["GROQ_TRANSCRIPTION_MODEL"]

    def _groq_transcript(self, audiopath: str):
        """
        Given a prompt, transcribe the audio file.
        """

        audiofile = open(audiopath, "rb")
        transcript = transcription(
            model=self.GROQ_TRANSCRIPTION_MODEL,
            file=audiofile,
            prompt=GROQ_AUDIO_PROMPT,
            response_format="text",
            temperature=0,
        )
        print(f"transcript: {transcript}")
        return transcript

    def podcastTransript(self, query: str) -> List[Podcast]:
        podcasts = searchservice.search(query=query)

        def generate_transcript(podcast):
            if podcast.audiopath:
                transcript = self._groq_transcript(audiopath=podcast.audiopath)
                print(f"transcript(concurrency): {transcript}")
                podcast.transcript = transcript.text
            return podcast

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            pd_transcripts = list(executor.map(generate_transcript, podcasts))

        return pd_transcripts
