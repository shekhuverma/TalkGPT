import asyncio

from openai import AsyncOpenAI, AuthenticationError, OpenAI

from ...exceptions import InvalidToken
from ...stream import PyAudioOutputStream
from .base import BaseTTS

op_queue = asyncio.Queue()


class OpenAiTTSEngine(BaseTTS):
    def __init__(
        self,
        API_KEY: str,
        op_stream: PyAudioOutputStream,
    ) -> None:
        self.API_KEY = API_KEY
        self.op_stream = op_stream

        self._validate_credentials()

        self.openai_ = AsyncOpenAI(api_key=self.API_KEY)

        # starting the audio streaming
        self.op_stream.start()

    def return_queue(self) -> asyncio.Queue:
        return op_queue

    def _validate_credentials(self):
        client = OpenAI(api_key=self.API_KEY)
        try:
            client.models.list()
        except AuthenticationError:
            raise InvalidToken(f"The provided API key {self.API_KEY} is incorrect!")

    # https://github.com/openai/openai-python#async-usage
    # Read this and see if i can attempt to create one
    async def process_prompt(self, prompt: str):
        async with self.openai_.audio.speech.with_streaming_response.create(
            model="tts-1",
            input=prompt,
            voice="echo",
            response_format="wav",
            speed=1,
        ) as response:
            # Syncing the PyAudioOutputStream chuck size here
            async for data in response.iter_bytes(self.op_stream.chunk_size):
                # await op_queue.put(data)
                await self.op_stream.write(data)
