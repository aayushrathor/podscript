# PodScript

> Generate Postcast transcription using AI

## TODO:

- [ ] Validation
- [ ] Spotify and Apple Podcast
- [ ] Containerization
- [ ] Frontend

## Setup

Create `.env` file in backend directory

```bash
GROQ_API_KEY=gsk_...
GROQ_TEXT_MODEL=groq/llama-3.1-8b-instant
GROQ_TRANSCRIPTION_MODEL=groq/whisper-large-v3
```

Run application

```bash
git clone https://github.com/aayushrathor/podscript.git
cd backend
uv pip install -r requirements.txt
python3 main.py
```
