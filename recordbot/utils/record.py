
from recordbot.apis.record import Api, Station, StreamTypes
from recordbot.utils.audio import Audio, AudioData, AudioFactory, Player


class RecordStreamData(AudioData):

    def __init__(self, station: Station, stream_type):
        self.station = station
        self.stream_type = stream_type

    @property
    def stream(self):
        return self.station.get_stream(self.stream_type)


class RecordStream(Audio):
    pass


class RecordAudioFactory(AudioFactory):

    async def get_data(self, prefix, stream=StreamTypes.S320):
        station = await Api.get_station(prefix)
        if station:
            return RecordStreamData(station, stream)

    async def get_source(self, data: RecordStreamData) -> RecordStream:
        return RecordStream(data)


class RecordPlayer(Player):
    factory = RecordAudioFactory()
