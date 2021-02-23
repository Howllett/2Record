
from aiohttp import ClientSession, TCPConnector
from urllib.parse import urlencode
from discord.utils import get


RECORD_API = "https://www.radiorecord.ru/api/{action}?{query}"


class RecordAPIError(Exception):
    pass


class Track:

    def __init__(self, data):
        self._data = data

    @property
    def _track(self):
        return self._data.get("track")

    @property
    def station_id(self):
        return self._data.get("id")

    @property
    def song(self):
        return self._track.get("song")

    @property
    def image(self):
        return self._track.get("image100")

    @property
    def artist(self):
        return self._track.get("artist")


class StreamTypes:
    S64 = "stream_64"
    S128 = "stream_128"
    S320 = "stream_320"


class Station:

    def __init__(self, data: dict):
        self._data = data

    def __repr__(self):
        return "<Station id=%s prefix=%s>" % (self.id, self.prefix)

    @property
    def id(self):
        return self._data.get("id")

    @property
    def prefix(self):
        return self._data.get("prefix")

    @property
    def icon(self):
        return self._data.get("icon_fill_colored")

    @property
    def title(self):
        return self._data.get("title")

    @property
    def tooltip(self):
        return self._data.get("tooltip")

    def get_stream(self, stream_type):
        return self._data.get(stream_type)


class RecordMinimalAPI:

    def __init__(self):
        self._session: ClientSession = ClientSession(
            connector=TCPConnector(ssl=False))

    def _form_query(self, query: str) -> str:
        return urlencode(query)

    def _form_request(self, action: str, query: str) -> str:
        return RECORD_API.format(
            action=action, query=self._form_query(query))

    async def _make_request(self, action: str, query: str) -> dict:
        request: str = self._form_request(action, query)
        async with self._session.get(request) as responce:
            resp = await responce.json()
            if not self.is_successful(resp):
                raise RecordAPIError(resp["error"]["message"])
            return resp["result"]

    def is_successful(self, resp) -> bool:
        return not ("error" in resp)

    async def get_station(self, prefix) -> Station:
        """Get stations by any given parameter

        Basic parameters:
        * prefix

        """
        return get(await self.get_stations(), prefix=prefix)

    async def _get_stations(self) -> list:
        return (await self._make_request("stations", {}))["stations"]

    async def get_stations(self) -> list:
        return [Station(st) for st in await self._get_stations()]

    async def get_now(self, station_id) -> Track:
        return get(await self.get_nows(), station_id=station_id)

    async def get_nows(self) -> list:
        return [
            Track(nw) for nw in await self._make_request("stations/now", {})]

    def close(self):
        self._session.close()


Api = RecordMinimalAPI()
