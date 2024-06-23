import asyncio
from asyncio import QueueEmpty

import colorama

from .llm import LLMEngine
from .speech_to_txt import STTEngine
from .stream import PyAudioInputStream, PyAudioOutputStream
from .txt_to_speech import TTSEngine

colorama.init(autoreset=True)


class TalkGPT:
    def __init__(
        self,
        ip: PyAudioInputStream,
        op: PyAudioOutputStream,
        stt_engine: STTEngine,
        llm_engine: LLMEngine,
        tts_engine: TTSEngine,
    ) -> None:
        if not isinstance(ip, PyAudioInputStream):
            raise TypeError("Input must be of type PyAudioInputStream")

        if not isinstance(op, PyAudioOutputStream):
            raise TypeError("Input must be of type PyAudioOutputStream")

        self.ip = ip
        self.op = op
        self.stt_engine: STTEngine = stt_engine
        self.llm_engine: LLMEngine = llm_engine
        self.tts_engine: TTSEngine = tts_engine
        self.stt_queue: asyncio.Queue
        self.tts_queue: asyncio.Queue
        self.stop_event = asyncio.Event()

        # Initialising the STT engine
        self.stt_engine.initialise(self.ip)
        print(colorama.Fore.GREEN + "STT Initialised!")

        # Initialise the LLM
        self.llm_engine.initialise()
        print(colorama.Fore.GREEN + "LLM Initialised!")

        # # Initialise the TTS
        self.tts_engine.initialise(self.op)
        print(colorama.Fore.GREEN + "TTS Initialised!")

    # # Takes the data from Queue and process it
    async def listenting(self, stop_event: asyncio.Event()):
        while not stop_event.is_set():
            try:
                x = self.stt_queue.get_nowait()
                llm_result = await self.llm_engine.process(x)
                await self.tts_engine.process(llm_result)
                self.stt_queue.task_done()
            except QueueEmpty:
                continue
            await asyncio.sleep(1)

    # Note to self: This section is not working, need to figure out why later on
    # Takes the data from Queue and process it
    # async def testing(self):
    #     while True:
    #         x = await self.stt_queue.get()
    #         await self.llm_engine.process(x)
    #         self.stt_queue.task_done()

    #         await asyncio.sleep(1)

    async def start(self):
        # Adding all the speech to text sentences to main queue
        self.stt_queue = self.stt_engine.start()

        T1 = asyncio.create_task(self.listenting(self.stop_event))

        # For a cleaner exit only
        try:
            await asyncio.gather(T1)
        except asyncio.CancelledError:
            T1.cancel()
            print(colorama.Fore.BLUE + "Shutting Down")

    def stop(self):
        # Stopping the STT engine
        self.stt_engine.stop()
        self.op.close()
