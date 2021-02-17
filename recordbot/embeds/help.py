
from discord import Guild
from discord.utils import get
from recordbot.embed import RecordEmbed

STATIONS_TITLE = "Станции %s/%s"
STATIONS_PATTERN = "%s `%s` %s"


class RecordStationsList(RecordEmbed):

    def __init__(self, holder: Guild, stations: list, page: int):
        start, end, desc = self._enumerate_stations(holder, stations, page)
        super().__init__(
            title=STATIONS_TITLE % (start, end),
            description=desc)

    def _find_emoji(self, holder: Guild, name: str):
        """Find emoji on emoji holder by station's prefix
        """
        return get(holder.emojis, name=name)

    def _enumerate_stations(
            self, holder: Guild, stations: list, page: int) -> str:
        """Enumerate each Record station with pairs of title and prefix

        This method returns start and end of list and formatted string of 10
        stations with title and prefix:

            * `Record` record

        Where the `Record` is title and `record` is prefix. `*` is reserved
        emoji of this station.

        """
        strings = []
        start = 10 * page
        end = start + 10
        # Stations count is 76 by default
        stations_size = len(stations)
        # When user requires page `7` the end of list is 80, what
        # is bigger than default stations count, so increase end's offset
        # to 76.
        if end > stations_size:
            if end - stations_size > 10:
                # Raise error when the page index out of range (Max 7).
                raise IndexError("Page count out of range (%s)." % page)
            end -= (end - stations_size)
        for station in stations[start:end]:
            title = station.get("title")
            prefix = station.get("prefix")
            if "-" in prefix:
                prefix = prefix.replace("-", "_")
            emoji = self._find_emoji(holder, prefix)
            if not emoji:
                emoji = "*"
            strings.append(STATIONS_PATTERN % (emoji, title, prefix))
        return start, end, "\n".join(strings)
