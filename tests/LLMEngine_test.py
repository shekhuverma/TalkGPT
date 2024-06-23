import pytest

from talkgpt.exceptions import InvalidToken, Unsupported
from talkgpt.llm import LLMEngine


def test_unsupported_engine():
    llm_engine = LLMEngine("closeAI", "abcdefgh")
    with pytest.raises(Unsupported, match="closeAI"):
        llm_engine.initialise()


def test_invalid_key():
    llm_engine = LLMEngine("OpenAI", "abcdefgh")
    with pytest.raises(InvalidToken, match="abcdefgh"):
        llm_engine.initialise()
