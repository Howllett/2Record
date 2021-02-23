
from recordbot.embed import RecordEmbed
from recordbot.apis.record import Station, Track


class RecordNowEmbed(RecordEmbed):

    def __init__(self, data: Track):
        super().__init__(title=data.song, description=data.artist)
        self.set_thumbnail(url=data.image)


class RecordAudioEmbed(RecordEmbed):

    def __init__(self, data: Station):
        super().__init__(title=data.title, description=data.tooltip)
        self.set_thumbnail(url=data.icon)
