
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

    async def get_data(self, query: str):
        return AudioData(query)

    def get_source(self, data: AudioData):
        return Audio(data)


class Player:

    def __init__(self, factory):
        self._factory = factory

    async def play(self, ctx: Context, *query, on_playing: Callable = None):
        """Play audio stream
        """
        data = await self._factory.get_data(*query)
        # Get source with certain audio data
        source = await self._factory.get_source(data)
        vclient = ctx.voice_client
        if vclient.is_playing():
            await self.stop(ctx)
        vclient.play(source)
        if on_playing:
            await on_playing(ctx, data)

    async def stop(self, ctx: Context, on_stopped: Callable = None):
        ctx.voice_client.stop()
        if on_stopped:
            await on_stopped(ctx)
