
#  ___ _____ _____ ____  _____ _____
# |_  |  _  |  |  |    \|     |     |
# |  _|     |  |  |  |  |-   -|  |  |
# |___|__|__|_____|____/|_____|_____|
# 2AUDIO Utility Module (UPDATED & SIMPLIFIED)
#

from os import name
from typing import Callable
from discord import FFmpegPCMAudio
from discord.ext.commands import Context


class AudioData:

    def __init__(self, url):
        self.url = url

    @property
    def stream(self):
        return self.url


class Audio(FFmpegPCMAudio):

    def __init__(self, data: AudioData):
        self.data = data
        # FFMpeg binaries required on Windows
        if name == "nt":
            executable = "bin/ffmpeg.exe"
        else:
            executable = "ffmpeg"
        super().__init__(source=self.data.stream, executable=executable)


class AudioFactory:

    def get_data(self, url: str):
        return AudioData(url)

    def get_source(self, data: AudioData):
        return Audio(data)


class Player:

    data: AudioData = None
    """Shortcut to source's audio data
    """

    source: Audio = None
    """Current playing source
    """

    factory: AudioFactory = AudioFactory()
    """Certain audio factory

    Allows to create new instance of Audio class.

    """

    async def play(self, ctx: Context, *query, on_playing: Callable = None):
        """Play audio stream
        """
        self.data = await self.factory.get_data(*query)
        # Get source with certain audio data
        self.source = await self.factory.get_source(self.data)
        vclient = ctx.voice_client
        if vclient.is_playing():
            await self.stop(ctx)
        vclient.play(self.source)
        if on_playing:
            await on_playing(ctx, self.data)

    async def stop(self, ctx: Context, on_stopped: Callable = None):
        ctx.voice_client.stop()
        if on_stopped:
            await on_stopped(ctx)
