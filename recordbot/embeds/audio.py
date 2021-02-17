
from recordbot.embed import RecordEmbed
from recordbot.utils.record import RecordStation


class RecordAudioLoading(RecordEmbed):

    def __init__(self):
        super().__init__(title="Загрузка")
        self.set_thumbnail(url="https://filmdar.com/tms-loading.gif")


class RecordAudioEmbed(RecordEmbed):

    def __init__(self, data: RecordStation):
        super().__init__(title=data.title, description=data.tooltip)
        self.set_thumbnail(url=data.icon)
        self.set_footer(text=data.stream)
