
# LiveKit Lesson Assistant

A simple agent created by LiveKit to answer questions in Polish about the lesson data provided by the pdf.

## Installation and configuration
First, create a virtual environment, update pip, and install the required packages:

```bash
$ python -m venv .venv
$ .venv\Scripts\activate
$ python -m pip install --upgrade pip
$ pip install livekit-agents[groq,silero,eleven]~=1.0rc
$ pip install python-dotenv
$ pip install pymupdf
```

You need to add file .env based on .env.example and set up the following environment variables:
```bash
LIVEKIT_URL=... 
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
GROQ_API_KEY=...
ELEVEN_API_KEY=...
LESSON_PDF_PATH=...
GROQ_LLM_MODEL="llama-3.3-70b-versatile"
```

You need to have accounts on: https://cloud.livekit.io/ and https://console.groq.com/ to have api keys and api key from: https://developers.deepgram.com/.

Then, run the assistant:
```bash
$ python lesson-assistant.py dev
  (dev for development mode or start for production mode)
```

Finally, you can load the [hosted playground](https://agents-playground.livekit.io/) and connect it.

## Usage

Based on the data in the file, the agent answers questions:
- „Czego dotyczy lekcja?”
- „Jakie są cele edukacyjne?”
- „Jakie aktywności zaplanowano dla uczniów?”
- "Ile trwa lekcja?"
- "Dla jakiej grupy wiekowej jest porzezaczona?"