from datetime import datetime, timezone
import httpx
from .config import Settings
from .schemas import Place, SourceRecord, WeatherSnapshot, InfrastructureSummary

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class DataSourceError(RuntimeError):
    pass

class PublicDataCollector:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.headers = {"User-Agent": self.settings.user_agent}

    async def _get_json(self, url: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=self.settings.timeout_seconds, headers=self.headers) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise DataSourceError(f"Unexpected response from {url}")
            return payload

    async def geocode(self, query: str) -> tuple[Place, SourceRecord]:
        if not query.strip():
            raise ValueError("Place must not be empty.")
        url = self.settings.geocoding_url
        payload = await self._get_json(url, {
            "name": query, "count": 5, "language": "en", "format": "json"
        })
        results = payload.get("results") or []
        if not results:
            raise DataSourceError(f"No geocoding result for {query!r}")
        # Exact/first provider-ranked match is shown to the user; no silent district inference.
        item = results[0]
        place = Place(
            name=item.get("name") or query,
            country=item.get("country"),
            admin1=item.get("admin1"),
            latitude=item["latitude"],
            longitude=item["longitude"],
            timezone=item.get("timezone"),
        )
        source = SourceRecord(provider="Open-Meteo Geocoding", url=url, status="success",
                              detail=f"Search query: {query}; selected first provider-ranked result.")
        return place, source

    async def weather(self, place: Place, forecast_days: int = 2) -> WeatherSnapshot:
        if not 1 <= forecast_days <= 7:
            raise ValueError("forecast_days must be between 1 and 7.")
        url = self.settings.forecast_url
        payload = await self._get_json(url, {
            "latitude": place.latitude,
            "longitude": place.longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_gusts_10m",
            "hourly": "precipitation_probability,precipitation,wind_gusts_10m",
            "forecast_days": forecast_days,
            "timezone": "auto",
        })
        current = payload.get("current")
        hourly = payload.get("hourly")
        if not isinstance(current, dict) or not isinstance(hourly, dict):
            raise DataSourceError("Weather provider response is missing current/hourly data.")
        if not hourly.get("time"):
            raise DataSourceError("Weather provider returned no hourly timestamps.")
        source = SourceRecord(provider="Open-Meteo Forecast API", url=url, status="success",
                              detail=f"Coordinates: {place.latitude},{place.longitude}; forecast_days={forecast_days}.")
        return WeatherSnapshot(current=current, hourly=hourly,
                               units=payload.get("hourly_units", {}), source=source)

    async def infrastructure(self, place: Place, radius_m: int = 5000) -> InfrastructureSummary:
        if not 500 <= radius_m <= 10000:
            raise ValueError("radius_m must be between 500 and 10000.")
        url = self.settings.overpass_url
        # Bounded query: only nearby healthcare/emergency-service features, not a bulk regional download.
        query = f'''[out:json][timeout:20];
(
  node(around:{radius_m},{place.latitude},{place.longitude})[amenity~"^(hospital|clinic|doctors)$"];
  way(around:{radius_m},{place.latitude},{place.longitude})[amenity~"^(hospital|clinic|doctors)$"];
  relation(around:{radius_m},{place.latitude},{place.longitude})[amenity~"^(hospital|clinic|doctors)$"];
  node(around:{radius_m},{place.latitude},{place.longitude})[emergency~"^(fire_station|ambulance_station)$"];
  way(around:{radius_m},{place.latitude},{place.longitude})[emergency~"^(fire_station|ambulance_station)$"];
  relation(around:{radius_m},{place.latitude},{place.longitude})[emergency~"^(fire_station|ambulance_station)$"];
);
out center tags;'''
        try:
            async with httpx.AsyncClient(timeout=self.settings.timeout_seconds,
                                         headers=self.headers) as client:
                response = await client.post(url, data={"data": query})
                response.raise_for_status()
                payload = response.json()
            elements = payload.get("elements", [])
            counts = {"hospital": 0, "clinic_or_doctor": 0, "fire_station": 0, "ambulance_station": 0}
            seen = set()
            for element in elements:
                key = (element.get("type"), element.get("id"))
                if key in seen:
                    continue
                seen.add(key)
                tags = element.get("tags") or {}
                amenity, emergency = tags.get("amenity"), tags.get("emergency")
                if amenity == "hospital":
                    counts["hospital"] += 1
                elif amenity in ("clinic", "doctors"):
                    counts["clinic_or_doctor"] += 1
                elif emergency == "fire_station":
                    counts["fire_station"] += 1
                elif emergency == "ambulance_station":
                    counts["ambulance_station"] += 1
            source = SourceRecord(provider="OpenStreetMap Overpass API", url=url, status="success",
                                  detail=f"Bounded radius query: {radius_m} metres.")
            return InfrastructureSummary(queried=True, radius_m=radius_m, counts=counts, source=source)
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            source = SourceRecord(provider="OpenStreetMap Overpass API", url=url, status="unavailable",
                                  detail=f"Source unavailable: {type(exc).__name__}: {exc}")
            return InfrastructureSummary(queried=False, radius_m=radius_m, counts={}, source=source,
                note="Infrastructure lookup failed or was unavailable. No facility count is inferred.")
