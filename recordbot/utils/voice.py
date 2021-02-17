
"""VOICE SHORTCUTS

3 basic shortcuts:
 * getclient
 * connect
 * disconnect

"""

from discord import VoiceClient, VoiceState
from discord.utils import get
from discord.ext.commands import Context


async def getclient(ctx: Context) -> VoiceClient:
    """Get voice client

    Tries to get a voice client of the current guild that bot
    is already connected to.

    """
    return get(ctx.bot.voice_clients, guild=ctx.guild)


async def connect(ctx: Context):
    """Connect to voice channel

    Connect to voice channel where the user who invoked command is.

    """
    vstate: VoiceState = ctx.author.voice
    if vstate:
        await vstate.channel.connect()


async def disconnect(ctx: Context):
    """Disconnect from voice channel

    """
    await ctx.voice_client.disconnect()
