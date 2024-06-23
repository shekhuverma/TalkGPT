from ..exceptions import Unsupported
from .engines.deepgram_engine import DeepgramEngine


class STTEngine:
    """Use to generate the STT object. Currently Only Deepgram is supported

    Raises:
        Unsupported: When any other engine is used other then OpenAI
    """

    # using dictionary for scalibility, just add the Engine class, no need to implement anything
    supported_engines = {"Deepgram": DeepgramEngine}

    def __init__(self, name, API_KEY) -> None:
        self.name = name
        self.API_KEY = API_KEY
        self.engine = None
        self.ip_stream = None

    # Initialising Deepgram
    def initialise(self, ip_stream) -> None:
        """Initialises the underlying TTS engine. Currently Only Deepgram is supported.
        For more info :- https://deepgram.com/

        Arguments:
            ip_stream -- output stream object of type PyAudioOutputStream

        Raises:
            Unsupported: When any other engine is used other then OpenAI
        """
        if self.name not in self.supported_engines:
            raise Unsupported(
                f"""The given engine "{self.name}" is not supported! \nCurrently we are only
                supporting the following engines {[_ for _ in STTEngine.supported_engines]}."""
            )
        self.ip_stream = ip_stream

        # Initialising deepgram and passing the input audio stream
        self.engine = STTEngine.supported_engines[self.name](
            self.API_KEY, self.ip_stream
        )

    # Starting Deepgram
    def start(self) -> None:
        # Will return the STT queue which will have all the sentences from speech
        return self.engine.start()

    def stop(self) -> None:
        """Closes the STT engine and IP stream."""
        self.engine.stop()
