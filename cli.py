import asyncio
import os

from dotenv import load_dotenv

from talkgpt import TalkGPT
from talkgpt.llm import LLMEngine
from talkgpt.speech_to_txt import STTEngine
from talkgpt.stream import PyAudioInputStream, PyAudioOutputStream
from talkgpt.txt_to_speech import TTSEngine

load_dotenv()
DEEPGRAM_KEY = os.getenv("DEEPGRAM_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

if DEEPGRAM_KEY is None or OPEN_AI_KEY is None:
    print("Please set the environment variables before continuing")
    print("Add variables in template.env and rename it to .env")
    exit(0)


ip_stream = PyAudioInputStream(sample_rate=22050, chunk_size=2048)

op_stream = PyAudioOutputStream(sample_rate=22050, chunk_size=2048)

stt_client = STTEngine("Deepgram", DEEPGRAM_KEY)

llm_client = LLMEngine("OpenAI", OPEN_AI_KEY)

tts_client = TTSEngine("OpenAI", OPEN_AI_KEY)


agent = TalkGPT(
    ip=ip_stream,
    op=op_stream,
    stt_engine=stt_client,
    llm_engine=llm_client,
    tts_engine=tts_client,
)

try:
    input("Press Enter Key to start speaking. Hit ctrl + C to stop")
    asyncio.run(agent.start())
except KeyboardInterrupt:
    agent.stop()
    exit(0)
