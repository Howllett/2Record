

from discord import Member, VoiceState, VoiceClient
from discord.utils import get
from discord.ext.commands import Bot
from recordbot.cogs.help import Help
from recordbot.cogs.audio import Audio


class RecordBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.remove_command("help")

        self.add_cog(Help())
        self.add_cog(Audio())

    async def on_voice_state_update(
            self, member: Member, before: VoiceState, after: VoiceState):
        # get audio cog to destroy last embed
        audio = self.get_cog("Audio")
        # Receive voice client
        vclient: VoiceClient = get(self.voice_clients, guild=member.guild)
        if not vclient:
            return
        # Bot automatically disconnects when the voice channel is empty
        if vclient.channel == before.channel:
            if not after.channel and len(before.channel.members) < 2:
                await audio.destroy_embed()
                await vclient.disconnect()
