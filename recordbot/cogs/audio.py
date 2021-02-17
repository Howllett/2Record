
from discord.ext.commands import Cog, command, Context
from recordbot.utils.audio import Player
from recordbot.utils.voice import getclient, connect, disconnect
from recordbot.utils.record import StreamTypes, RecordAudioFactory
from recordbot.embeds.audio import RecordAudioEmbed


class Audio(Cog):

    player = Player(RecordAudioFactory())

    _embed = None

    async def show_embed(self, ctx, data):
        self._embed = await ctx.send(embed=RecordAudioEmbed(data))

    async def destroy_embed(self, *args):
        if self._embed:
            await self._embed.delete()

    @command(name="join", aliases=["j"])
    async def command_join(self, ctx: Context):
        await connect(ctx)

    @command(name="play", aliases=["pl", "p"])
    async def command_play(self, ctx: Context, name, stream: int = 320):
        vclient = await getclient(ctx)
        if not vclient:
            vclient = await connect(ctx)
        # Select stream quality and give it qualified name, such as:
        # `stream_64` instead of 64, `stream_128` instead of 128 and e. t. c.
        if stream == 64:
            stream = StreamTypes.S64
        elif stream == 128:
            stream = StreamTypes.S128
        elif stream == 320:
            stream = StreamTypes.S320
        # Play audio with certain stream quality
        await self.player.play(ctx, name, stream, on_playing=self.show_embed)

    @command(name="stop", aliases=["stp", "st", "s"])
    async def command_stop(self, ctx):
        await self.player.stop(ctx, self.destroy_embed)

    @command(name="leave", aliases=["lv", "l"])
    async def command_leave(self, ctx):
        await disconnect(ctx)
