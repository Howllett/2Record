
import pytest
from aiohttp import ClientSession, TCPConnector
from recordbot.apis.record import RecordMinimalAPI

record_api: RecordMinimalAPI

asyncio = pytest.mark.asyncio


def setup():
    global record_api
    session = ClientSession(connector=TCPConnector(ssl=False))
    record_api = RecordMinimalAPI(session)


@asyncio
async def test_get_stations():
    await record_api.get_stations()
