import asyncio
import httpx
from civicpulse.api import app


def test_health_endpoint_is_available_without_external_data_calls():
    async def run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["agent"] == "civicpulse-ai"
    asyncio.run(run())
