from ..exceptions import Unsupported
from .engines.openai_tts_engine import OpenAiTTSEngine


class TTSEngine:
    """A class to interface with various Language Model Engines (LLM).
    Currently, it supports the OpenAI engine.

    Raises:
        Unsupported: Raised when any other engine is used other then OpenAI
    """

    # using dictionary for scalibility, just add the Engine class, no need to implement anything
    supported_engines = {"OpenAI": OpenAiTTSEngine}

    def __init__(self, name, API_KEY) -> None:
        self.name = name
        self.API_KEY = API_KEY
        self.op_stream = None
        self.engine = None

    # Initialising OpenAI TTS
    def initialise(self, op_stream) -> None:
        """Initialises the underlying TTS engine. Currently Only OpenAI is supported

        Arguments:
            op_stream -- output stream object of type PyAudioOutputStream

        Raises:
            Unsupported: When any other engine is used other then OpenAI
        """
        if self.name not in self.supported_engines:
            raise Unsupported(
                f"""The given engine "{self.name}" is not supported! \n Currently we are only
                supporting the following engines {[_ for _ in TTSEngine.supported_engines]}."""
            )

        self.op_stream = op_stream

        # Initialising deepgram and passing the input audio stream
        self.engine = TTSEngine.supported_engines[self.name](
            self.API_KEY, self.op_stream
        )

    # Starting OpenAI TTS
    async def process(self, prompt) -> None:
        await self.engine.process_prompt(prompt)

    # def stop(self) -> None:
    #     self.engine.stop()
