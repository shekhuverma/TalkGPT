import pytest

from talkgpt.exceptions import InvalidToken, Unsupported
from talkgpt.txt_to_speech import TTSEngine


def test_unsupported_engine():
    tts_engine = TTSEngine("closeAI", "abcdefgh")
    with pytest.raises(Unsupported, match="closeAI"):
        tts_engine.initialise(None)


def test_invalid_key():
    tts_engine = TTSEngine("OpenAI", "abcdefgh")
    with pytest.raises(InvalidToken, match="abcdefgh"):
        tts_engine.initialise(None)
