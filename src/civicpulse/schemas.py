from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Place(BaseModel):
    name: str
    country: str | None = None
    admin1: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str | None = None

class SourceRecord(BaseModel):
    provider: str
    url: str
    retrieved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str
    detail: str | None = None

class InfrastructureSummary(BaseModel):
    queried: bool
    radius_m: int
    counts: dict[str, int] = Field(default_factory=dict)
    source: SourceRecord
    note: str = "Mapped feature counts are not verified capacity or availability."

class WeatherSnapshot(BaseModel):
    current: dict
    hourly: dict
    units: dict
    source: SourceRecord

class AnalysisResult(BaseModel):
    place: Place
    geocoding_source: SourceRecord
    weather: WeatherSnapshot
    infrastructure: InfrastructureSummary
    screening_score: int | None
    screening_label: str
    components: dict[str, float | None]
    explanation: list[str]
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    human_review_required: bool = True
