import pytest

from talkgpt.exceptions import InvalidToken, Unsupported
from talkgpt.speech_to_txt import STTEngine


def test_unsupported_engine():
    stt_engine = STTEngine("eepgram", "abcdefgh")
    with pytest.raises(Unsupported, match="eepgram"):
        stt_engine.initialise(None)


def test_invalid_key():
    stt_engine = STTEngine("Deepgram", "abcdefgh")
    with pytest.raises(InvalidToken, match="abcdefgh"):
        stt_engine.initialise(None)
