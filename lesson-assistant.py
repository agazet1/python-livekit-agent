import os
import logging
import fitz
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import groq, silero, elevenlabs
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("lesson-assistant")

def get_lesson_pdf(pdf_path):
    return get_text(pdf_path)

def get_text(pdf_path):
    pdf_document = fitz.open(pdf_path)

    full_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        full_text += text
    return full_text


async def entrypoint(ctx: JobContext):

    llm_model=os.getenv("GROQ_LLM_MODEL")    
    pdf_path=os.getenv("LESSON_PDF_PATH")
    pdf_txt = get_lesson_pdf(pdf_path)

    if llm_model=="" or pdf_path=="" or pdf_txt=="":
        logger.error("Missing variables in .env file.")

    await ctx.connect()

    agent = Agent(
        instructions="""
            You are a friendly voice assistant built by LiveKit. You speak and write to the user in Polish.
            You should provide answers about lesson if the question is about:  what the lesson is about, what are the learning goals, what activities are planned for the students, what age group is it for or how long the lesson lasts. 
            Otherwise, offer that you can answer one of the above questions."""
            "Each answer should be short and concise and be no more than 4-5 sentences long or maximum 2 where question is about time or age."
            f"You answears base only on data from text: {pdf_txt}. If the source text is empty, only reply to each question by stating that the data is missing",
    )

    session = AgentSession(
        vad=silero.VAD.load(
            min_speech_duration=0.2,
            min_silence_duration=0.6
        ),
        # any combination of STT, LLM, TTS, or realtime API can be used
        stt=groq.STT(language="pl"),  
        llm=groq.LLM(model=llm_model),
        tts=elevenlabs.TTS(
            voice_id="ODq5zmih8GrVes37Dizd",
            model="eleven_multilingual_v2"
        )
    )

    await session.start(
        agent=agent, 
        room=ctx.room,
    )
    await session.generate_reply(instructions="Say hello, then ask the user how you can help about the Bathyscaphe lesson.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))