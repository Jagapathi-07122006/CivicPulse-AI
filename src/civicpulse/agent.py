from .collectors import PublicDataCollector
from .analyzer import build_analysis
from .report import render_markdown

class CivicPulseAgent:
    def __init__(self, collector=None):
        self.collector = collector or PublicDataCollector()

    async def analyze(self, place_query: str, radius_m: int = 5000, forecast_days: int = 2):
        place, geocode_source = await self.collector.geocode(place_query)
        weather = await self.collector.weather(place, forecast_days=forecast_days)
        infrastructure = await self.collector.infrastructure(place, radius_m=radius_m)
        result = build_analysis(place, geocode_source, weather, infrastructure)
        return result

    async def analyze_report(self, place_query: str, radius_m: int = 5000, forecast_days: int = 2):
        result = await self.analyze(place_query, radius_m, forecast_days)
        return result, render_markdown(result)
