import pyaudio


class PyAudioInputStream:
    def __init__(self, sample_rate: int, chunk_size: int):
        self.sample_rate = sample_rate
        self.__chunk_size = chunk_size
        self._callback_function = lambda data: None

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.__chunk_size,
            stream_callback=self._callback,
            start=False,  # To only start the stream after everything is setup
        )

    # Will be called in a seperate thread whenever there is some incoming data!
    # Reference - https://people.csail.mit.edu/hubert/pyaudio/docs/#id3
    def _callback(self, input_data, frame_count, time_info, status_flags):
        self._callback_function(input_data)
        # time.sleep(0.5)
        return input_data, pyaudio.paContinue

    def set_callback(self, function):
        self._callback_function = function

    def start(self):
        self.stream.start_stream()

    def read(self, chunk_size: int):
        return self.stream.read(chunk_size)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()


class PyAudioOutputStream:
    def __init__(self, sample_rate, chunk_size):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self._callback_function = lambda: None

        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=chunk_size,
            start=False,  # To only start the stream after everything is setup
        )

    def start(self):
        self.stream.start_stream()

    async def write(self, input_stream: PyAudioInputStream):
        return self.stream.write(input_stream)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
