
from recordbot.apis.record import Api
from recordbot.utils.audio import Audio, AudioData, AudioFactory


class StreamTypes:
    S64 = "stream_64"
    S128 = "stream_128"
    S320 = "stream_320"


class RecordAPIError(Exception):
    pass


class RecordAudio(Audio):
    pass


class RecordStation(AudioData):

    def __init__(self, data: dict, stream):
        self._data = data
        self._stream = stream

    @property
    def icon(self):
        return self._data.get("icon_fill_colored")

    @property
    def title(self):
        return self._data.get("title")

    @property
    def tooltip(self):
        return self._data.get("tooltip")

    @property
    def stream(self):
        if self._stream == StreamTypes.S64:
            return self.stream64
        elif self._stream == StreamTypes.S128:
            return self.stream128
        elif self._stream == StreamTypes.S320:
            return self.stream320

    @property
    def stream64(self):
        return self._data.get("stream_64")

    @property
    def stream128(self):
        return self._data.get("stream_128")

    @property
    def stream320(self):
        return self._data.get("stream_320")


class RecordAudioFactory(AudioFactory):

    async def get_data(self, prefix, stream=StreamTypes.S320) -> RecordStation:
        return RecordStation(await Api.get_station(prefix), stream)

    async def get_source(self, data: RecordStation) -> RecordAudio:
        return RecordAudio(data)
