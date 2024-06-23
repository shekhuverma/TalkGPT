import json
from time import perf_counter

import colorama
from openai import AsyncOpenAI, AuthenticationError, OpenAI

from talkgpt.exceptions import InvalidToken

colorama.init(autoreset=True)


class OpenAiEngine:
    def __init__(
        self,
        API_KEY: str,
    ) -> None:
        self.API_KEY = API_KEY

        self._validate_credentials()
        self.openai_ = AsyncOpenAI(api_key=self.API_KEY)

    def _validate_credentials(self):
        client = OpenAI(api_key=self.API_KEY)
        try:
            client.models.list()
        except AuthenticationError:
            raise InvalidToken(f"The provided API key {self.API_KEY} is incorrect!")

    # https://github.com/openai/openai-python#async-usage
    # Read this and see if i can attempt to create one
    async def process_prompt(self, prompt: str):
        result = ""
        t1 = perf_counter()
        first_response = None
        async with self.openai_.chat.completions.with_streaming_response.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Helpfull AI Assistant"},
                {"role": "user", "content": prompt},
            ],
        ) as response:
            async for chunk in response.iter_lines():
                if not first_response:
                    first_response = perf_counter()
                result += chunk

        end_time = perf_counter()
        print(
            colorama.Fore.BLUE
            + f"Time for First Token from LLM  = {(end_time-first_response):.2f} Sec"
        )
        print(
            colorama.Fore.BLUE
            + f"Time for Complete Response From LLM = {(end_time-t1):.2f} Sec"
        )
        result = json.loads(result)["choices"][0]["message"]["content"]
        print(colorama.Fore.MAGENTA + "LLM result:- ")
        print(result)
        return result
