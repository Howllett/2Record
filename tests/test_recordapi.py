
import pytest
from recordbot.apis.record import RecordMinimalAPI

use = pytest.mark.usefixture
async_ = pytest.mark.asyncio


SD90 = "sd90"  # Superdisco's prefix name
SD90_ID = 539  # Superdisco's station id


@pytest.fixture
def api():
    return RecordMinimalAPI()


@async_
async def test_get_now(api):
    await api.get_now(SD90)


@async_
async def test_get_station(api):
    await api.get_station(SD90)


@async_
async def test_get_stations(api):
    await api.get_stations()


@async_
async def test_get_station_info(api):
    station = await api.get_station(SD90)

    # Successfully got the station data
    assert station is not None
    # Station's id validation
    assert station.id == SD90_ID
    # Station's prefix name validation
    assert station.prefix == SD90
    # Test __repr__ magic method
    print(station)
