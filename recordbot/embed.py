
from discord import Embed


class RecordEmbed(Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, color=0xff6000, **kwargs)
