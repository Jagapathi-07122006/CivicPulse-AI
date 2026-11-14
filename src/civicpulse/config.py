from pydantic import BaseModel, Field

class Settings(BaseModel):
    geocoding_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    forecast_url: str = "https://api.open-meteo.com/v1/forecast"
    overpass_url: str = "https://overpass-api.de/api/interpreter"
    user_agent: str = "CivicPulseAI/0.1 (student research project)"
    timeout_seconds: float = Field(default=20.0, gt=0, le=60)
