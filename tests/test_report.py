from civicpulse.report import render_markdown
from civicpulse.schemas import Place, WeatherSnapshot, InfrastructureSummary, SourceRecord
from civicpulse.analyzer import build_analysis

def test_report_discloses_sources_and_limitations():
    place = Place(name="Unit-test place", latitude=16.5, longitude=80.6)
    weather = WeatherSnapshot(
        current={"temperature_2m": 29},
        hourly={"time": ["2030-01-01T00:00"], "precipitation_probability": [20],
                "precipitation": [1], "wind_gusts_10m": [10]},
        units={},
        source=SourceRecord(provider="test-vector", url="https://example.invalid", status="test-only")
    )
    geocode = SourceRecord(provider="Open-Meteo Geocoding", url="https://geocoding-api.open-meteo.com/v1/search", status="test-only")
    infra = InfrastructureSummary(
        queried=False, radius_m=5000, counts={},
        source=SourceRecord(provider="test-vector", url="https://example.invalid", status="unavailable")
    )
    report = render_markdown(build_analysis(place, geocode, weather, infra))
    assert "not a validated probability" in report
    assert "human reviewer" in report
    assert "Retrieved at" in report
    assert "Geocoding evidence" in report
    assert "OpenStreetMap" in report
