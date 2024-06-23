from ..exceptions import Unsupported
from .engines.openai_engine import OpenAiEngine


class LLMEngine:
    """A class to interface with various Language Model Engines (LLM).
    Currently, it supports the OpenAI engine.

    Raises:
        Unsupported: Raised when any other engine is used other then OpenAI
    """

    # using dictionary for scalibility, just add the Engine class, no need to implement anything
    supported_engines = {"OpenAI": OpenAiEngine}

    def __init__(self, name, API_KEY) -> None:
        self.name = name
        self.API_KEY = API_KEY
        self.engine = None

    # Initialising OpenAI LLM
    def initialise(self) -> None:
        """Initialises the underlying LLM engine. Currently Only OpenAI is supported

        Raises:
            Unsupported: When any other engine is used other then OpenAI
        """
        if self.name not in self.supported_engines:
            raise Unsupported(
                f"""The given engine "{self.name}" is not supported! \nCurrently we are only
                supporting the following engines {[_ for _ in LLMEngine.supported_engines]}."""
            )

        self.engine = LLMEngine.supported_engines[self.name](self.API_KEY)

    # Starting OpenAI LLM
    async def process(self, prompt) -> None:
        # Returns the result from LLM
        return await self.engine.process_prompt(prompt)
