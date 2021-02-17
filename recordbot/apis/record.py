
from aiohttp import ClientSession, TCPConnector
from urllib.parse import urlencode


RECORD_API = "https://www.radiorecord.ru/api/{action}?{query}"


class RecordAPIError(Exception):
    pass


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
            if "error" in resp:
                raise RecordAPIError(resp["error"]["message"])
            return resp["result"]

    async def get_station(self, prefix):
        """Get stations by any given parameter

        Basic parameters:
        * prefix

        """
        stations = await self.get_stations()
        for station in stations:
            if station.get("prefix") == prefix:
                return station

    async def get_stations(self) -> list:
        return (await self._make_request("stations", {}))["stations"]


Api = RecordMinimalAPI()
