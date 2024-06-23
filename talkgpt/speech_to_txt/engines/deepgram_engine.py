import asyncio
from time import perf_counter

import colorama

# import pyaudio
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
)
from deepgram.clients.live.v1.client import LiveClient

from talkgpt.exceptions import ConnectionFailed
from talkgpt.stream import PyAudioInputStream

from ...utils import validate_credentials_deepgram
from .base import BaseSTT

colorama.init(autoreset=True)
is_finals = []
stt_queue = asyncio.Queue()
t1 = 0


def on_open(self, open, **kwargs):
    print("Deepgram started!\nConnection Open")


def on_message(self, result, **kwargs):
    global is_finals, t1

    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    if result.is_final:
        # We need to collect these and concatenate them together when we get a speech_final=true
        # See docs: https://developers.deepgram.com/docs/understand-endpointing-interim-results
        is_finals.append(sentence)

        # Speech Final means we have detected sufficent silence to consider this end of speech
        # Speech final is the lowest latency result as it triggers as soon an the endpointing value has triggered
        if result.speech_final:
            utterance = " ".join(is_finals)
            asyncio.run(stt_queue.put(utterance))
            print(
                colorama.Fore.BLUE
                + f"Total time took by STT = {(perf_counter()-t1):.2f} seconds!"
            )
            print(f"Speech Final: {utterance}")
            is_finals = []
        else:
            # These are useful if you need real time captioning and update what the Interim Results produced
            print(f"Is Final: {sentence}")
            asyncio.run(stt_queue.put(sentence))
    else:
        # These are useful if you need real time captioning of what is being spoken
        print(f"Interim Results: {sentence}")


def on_metadata(self, metadata, **kwargs):
    # print(f"Metadata: {metadata}")
    pass


def on_speech_started(self, speech_started, **kwargs):
    global t1
    t1 = perf_counter()
    print("Speech Started")


def on_utterance_end(self, utterance_end, **kwargs):
    print("Utterance End")
    global is_finals
    if len(is_finals) > 0:
        utterance = " ".join(is_finals)
        print(f"Utterance End: {utterance}")
        is_finals = []


def on_close(self, close, **kwargs):
    print("Connection Closed")


def on_error(self, error, **kwargs):
    print(f"Handled Error: {error}")


def on_unhandled(self, unhandled, **kwargs):
    print(f"Unhandled Websocket Message: {unhandled}")


API_CONFIG: DeepgramClientOptions = DeepgramClientOptions(options={"keepalive": "true"})


class DeepgramEngine(BaseSTT):
    """The actual implementation of Deepgram Engine to be used by STTEngine"""

    def __init__(
        self,
        API_KEY: str,
        ip_stream: PyAudioInputStream,
        config: DeepgramClientOptions = API_CONFIG,
    ) -> None:
        self.API_KEY = API_KEY
        self.config = config
        self.ip_stream = ip_stream
        self.stt_queue = stt_queue
        self.connection: LiveClient = None

        # self._validate_credentials()
        self._initialise()

    def _validate_credentials(self):
        validate_credentials_deepgram(self.API_KEY)

    def _initialise(self):
        # Create a websocket connection using the DEEPGRAM_API_KEY from environment variables
        deepgram = DeepgramClient(self.API_KEY)

        # Use the listen.live class to create the websocket connection
        self.connection = deepgram.listen.live.v("1")

        self.connection.on(LiveTranscriptionEvents.Open, on_open)
        self.connection.on(LiveTranscriptionEvents.Transcript, on_message)
        self.connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        self.connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        self.connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        self.connection.on(LiveTranscriptionEvents.Close, on_close)
        self.connection.on(LiveTranscriptionEvents.Error, on_error)
        self.connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

    # Starting Deepgram
    def start(self):
        options: LiveOptions = LiveOptions(
            model="nova-2",
            language="en-US",
            # Apply smart formatting to the output
            smart_format=True,
            # Raw audio format deatils
            encoding="linear16",
            channels=1,
            # // sync the sample rates b/w PyAudioInputStream and here
            sample_rate=self.ip_stream.sample_rate,
            # To get UtteranceEnd, the following must be set:
            # interim_results=True,
            # utterance_end_ms="1000",
            # vad_events=True,
            interim_results=False,
            # utterance_end_ms="1000",
            # vad_events=True,
            # Time in milliseconds of silence to wait for before finalizing speech
            endpointing=200,
        )

        add_ons = {
            # Prevent waiting for additional numbers
            "no_delay": "true"
        }

        if self.connection.start(options, add_ons) is False:
            raise ConnectionFailed("Unable to connect to Deepgram")

        # Setting up the Pyaudio callback
        self.ip_stream.set_callback(self.connection.send)
        # starting the audio streaming
        self.ip_stream.start()

        return stt_queue

    def stop(self):
        """Closes the Deepgram STT engine and IP stream."""
        self.ip_stream.close()
        self.connection.finish()
