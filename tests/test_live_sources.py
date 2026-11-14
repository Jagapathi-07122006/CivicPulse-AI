import os
import pytest
from civicpulse.collectors import PublicDataCollector

pytestmark = pytest.mark.skipif(
    os.getenv("CIVICPULSE_LIVE_TESTS") != "1",
    reason="Set CIVICPULSE_LIVE_TESTS=1 to call real public APIs."
)

@pytest.mark.asyncio
async def test_live_geocoding_and_weather():
    collector = PublicDataCollector()
    place, source = await collector.geocode("Vijayawada, Andhra Pradesh, India")
    assert -90 <= place.latitude <= 90
    assert -180 <= place.longitude <= 180
    weather = await collector.weather(place, forecast_days=1)
    assert weather.source.status == "success"
    assert weather.hourly["time"]

@pytest.mark.asyncio
async def test_live_bounded_overpass_query():
    collector = PublicDataCollector()
    place, _ = await collector.geocode("Vijayawada, Andhra Pradesh, India")
    result = await collector.infrastructure(place, radius_m=1000)
    # Either a real response or an explicitly recorded provider outage is acceptable.
    assert result.source.status in {"success", "unavailable"}
    assert result.queried == (result.source.status == "success")
