
from discord import Guild
from discord.ext.commands import Cog, command, Context
from recordbot.meta import EMOJI_HOLDER, EMOJI_HOLDER2
from recordbot.apis.record import Api
from recordbot.embeds.help import RecordStationsList, RecordHelp


class Help(Cog):

    @command(name="help", aliases=["hlp", "hl", "h"])
    async def command_help(self, ctx: Context):
        await ctx.send(embed=RecordHelp)

    @command(name="list", aliases=["lst", "ls"])
    async def command_list(self, ctx: Context, page: int = 1):
        if page < 6:
            holder: Guild = await ctx.bot.fetch_guild(EMOJI_HOLDER)
        else:
            holder: Guild = await ctx.bot.fetch_guild(EMOJI_HOLDER2)
        await ctx.send(
            embed=RecordStationsList(
                holder,  # Emoji holder
                await Api.get_stations(),  # List of stations
                page - 1))  # Page decrased by 1
